import os
import re
import glob
import numpy as np
import pandas as pd

#Paths
DATA_FOLDER = r"C:\Users\asus\Desktop\Assignment2\temperatures"

AVG_FILE = "average_temp.txt"
RANGE_FILE = "largest_temp_range_station.txt"
STABILITY_FILE = "temperature_stability_stations.txt"

#This is the season 
SEASONS = {
    "Summer(Dec-Feb)": [12, 1, 2],
    "Autumn(Mar-May)": [3, 4, 5],
    "Winter(Jun-Aug)": [6, 7, 8],
    "Spring(Sep-Nov)": [9, 10, 11],
}
SEASON_ORDER = ["Summer(Dec-Feb)", "Autumn(Mar-May)", "Winter(Jun-Aug)", "Spring(Sep-Nov)"]

#This is the month name to number form 
MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}

#list of column name
MONTH_COLS = list(MONTH_MAP.keys())      

#Make all column names lowercase and remove extra spaces.
def _clean_headers(cols):
    return [str(c).strip().lower() for c in cols]

#we make a column into numbers if the invalid values become NaN we have to ignore it
def _to_number(s):
    return pd.to_numeric(s, errors="coerce")

 #Get a 4 digit year from the filename
def _year_from_filename(path):
    m = re.search(r"(\d{4})", os.path.basename(path))
    if not m:
        return None
    y = int(m.group(1))
    return y if 1800 <= y <= 2100 else None

#station name/IDs may use different headers we are trying common possiblities and return the first one that exits.
def _find_station_column(df):
    for cand in ["station_name", "station", "stn_id", "stn_idd", "site", "site_id", "name", "location"]:
        if cand in df.columns:
            return cand
    return None

#check if the file has january to december which will be in the wide format
def _is_wide_month_file(df):
    return all(m in df.columns for m in MONTH_COLS)

#Convert wide monthly table to a long table 
def _wide_months_to_long(df, file_path):
    year = _year_from_filename(file_path)
    if year is None:
        return pd.DataFrame(columns=["date", "station", "temperature"])

    st_col = _find_station_column(df)
    if not st_col:
        return pd.DataFrame(columns=["date", "station", "temperature"])

    cols = [st_col] + MONTH_COLS
    melted = df[cols].melt(id_vars=[st_col], value_vars=MONTH_COLS,
                           var_name="month_name", value_name="temperature")

    melted["station"] = melted[st_col].astype(str).str.strip()
    melted["temperature"] = _to_number(melted["temperature"])
    melted["month"] = melted["month_name"].map(MONTH_MAP).astype("Int64")


    # build a simple date at the first day of each month
    melted["date"] = pd.to_datetime(
        {"year": year, "month": melted["month"].astype("int"), "day": 1},
        errors="coerce"
    )

#Return only the columns we need drop missing station/temp
    out = melted[["date", "station", "temperature"]]
    out = out.dropna(subset=["station", "temperature"])
    return out


#Load all the data (folder)
def load_all_data(folder):
    files = glob.glob(os.path.join(folder, "*.csv"))
    if not files:
        print(f"No CSV files found in {folder}")
        return pd.DataFrame(columns=["date", "station", "temperature"])

    frames = []
    for fp in files:

        # Try to read the CSV (utf-8 first, then latin-1 if needed)
        try:
            df = pd.read_csv(fp, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(fp, encoding="latin-1")
        except Exception as e:
            print(f"Skipping {os.path.basename(fp)} (read error: {e})")
            continue

 # Normalize headers
        df.columns = _clean_headers(df.columns)

 # Case A: Your typical 'wide' monthly file
        if _is_wide_month_file(df):
            mini = _wide_months_to_long(df, fp)
            if mini.empty:
                print(f"Skipping {os.path.basename(fp)} (no usable rows after reshape)")
                continue
            frames.append(mini)
            continue

        # fallback for already-long formats (if any)
        st_col = _find_station_column(df)
        temp_col = next((c for c in ["temperature", "avg_temp", "temp", "tmean", "tavg", "t_avg"]
                         if c in df.columns), None)
        
  # Build a date if we can (from 'date' or year+month)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        elif "year" in df.columns and "month" in df.columns:
            df["date"] = pd.to_datetime(
                {"year": _to_number(df["year"]), "month": _to_number(df["month"]), "day": 1},
                errors="coerce"
            )
        else:
            df["date"] = pd.NaT

  # Keep only the needed columns; drop missing station/temperature
        if st_col and temp_col:
            mini = pd.DataFrame({
                "date": df["date"],
                "station": df[st_col].astype(str).str.strip(),
                "temperature": _to_number(df[temp_col]),
            }).dropna(subset=["station", "temperature"])
            if not mini.empty:
                frames.append(mini)
        else:
            print(f"Skipping {os.path.basename(fp)} (unrecognized columns)")

 # If nothing valid was loaded, return empty
    if not frames:
        print("No valid rows found after loading.")
        return pd.DataFrame(columns=["date", "station", "temperature"])
    
  # Combine all files into one table and remove exact duplicates
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset=["date", "station", "temperature"])
    return out

#Analysis 1 : Seasonal average 
def write_seasonal_average(df, out_path):
    """average temperature per season across all stations and years"""

     # Ignore rows with missing temperature
    work = df.dropna(subset=["temperature"]).copy()

    #We need valid dates to know which month/season each row is in
    if "date" not in work.columns or work["date"].isna().all():
        with open(out_path, "w", encoding="utf-8-sig") as f:
            f.write("No usable dates found to compute seasonal averages.\n")
        return
    
 # we Remove rows with missing dates
    work = work.dropna(subset=["date"])
    if work.empty:
        with open(out_path, "w", encoding="utf-8-sig") as f:
            f.write("No valid data found for seasonal averages.\n")
        return
    
#we are getting numeric month for each row
    work["month"] = work["date"].dt.month

    #we compute all the average for each season
    results = {}

    for season in SEASON_ORDER:
        months = SEASONS[season]
        season_df = work[work["month"].isin(months)]
        if not season_df.empty:
            avg_temp = season_df["temperature"].mean(skipna=True)
            if not np.isnan(avg_temp):
                results[season] = avg_temp

#we have to write the line per season to the oputput file 
    with open(out_path, "w", encoding="utf-8-sig") as f:
        if not results:
            f.write("No seasonal averages available.\n")
        else:
            for season in SEASON_ORDER:
                if season in results:
                    f.write(f"{season}: {results[season]:.1f}°C\n")

#Analysis 2 : Largest temperature range 
def write_largest_range(df, out_path):

    # finding station(s) with the largest temperature range (max - min)
    work = df.dropna(subset=["station", "temperature"]).copy()
    if work.empty:
        with open(out_path, "w", encoding="utf-8-sig") as f:
            f.write("No valid temperature data found.\n")
        return
    
#we are grouping all the data by station and find min and max
    grouped = work.groupby("station")["temperature"]
    stats = grouped.agg(["min", "max"])
    stats["range"] = stats["max"] - stats["min"]

#finding the largest value and select all stations that match it
    max_range = stats["range"].max()
    top = stats[stats["range"] == max_range].sort_index()

#we write each tied station in the required format
    with open(out_path, "w", encoding="utf-8-sig") as f:
        for st, row in top.iterrows():
            f.write(f"{st}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")
