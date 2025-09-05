import turtle 

def line_segment(length,depth):     #Creating a function for the line segment to generate a geometric pattern
    
    if depth==0:                    #for depth 0 it draws straignt line.
        turtle.fd(length)
   
    else:
        length= length/3              #Each line segment of a polygon is divided into 3 equal parts. 
       
        line_segment(length,depth-1)  #First edge of a line segment
       
        turtle.rt(60)                 #Rotates turtle 60 degree clockwise to draw the left side of an inward equilateral triangle(Second edge of a line segment).
       
        line_segment(length,depth-1)  #Left side of an equilateral triangle, replacing the middle segment.
        
        turtle.lt(120)                #Rotates turtle 120 degree counterclockwise to draw the right side of an inward equilateral triangle(Third edge of a line segment).
        
        line_segment(length,depth-1)  #Right side of an equilateral triangle.
        
        turtle.rt(60)                 #Rotates turtle 60 degrees clockwise to resume the original direction for the final edge of the segment.
        
        line_segment(length,depth-1)  #Final edge of a line segment



         

def polygon(sides,length,depth):     #Function to draw a regular polygon

    angle= 360/sides                 #Calculating angle for a regular polygon 

    for i in range(sides):           #for loop to draw a regular polygon

        line_segment(length,depth)   #Draws first side/line segment of a regular polygon
        turtle.rt(angle)             #Rotates angle degress clockwise to draw the next line segment of the same polygon.



#Main function
def main():
 
    try:    #try_Except to validate the user inputs.
        sides=int(input("Enter the number of sides of a regular polygon:: "))  #Asking user to input the sides of a regular polygon.
        if sides<3:
         print("Sides should not be less than 3")
         return
        

        length=int(input("Enter the length of a regular polygon(in pixels):: "))  #Asking user to input the length of a regular polygon(in pixels)
        if length <=0:
         print("Length should be positive")
         return
                
        depth=int(input("Enter the recursion depth to apply:: "))  #Asking user to input recursion depth i.e how many time we need to do recursion.
        if depth<0:
         print("Depth should be positive")
         return

        turtle.speed(0)                 # Setting up the maximum speed of the turtle
        turtle.shape("turtle")                               #Changing the shape
        turtle.title("Generating Geometric Pattern")         #Title of the graphics

         #Changing position of the turtle to start drawing.

        turtle.penup()                  #Lifts the pen i.e moves turtle without drawing.
        turtle.goto(-200,200)           #Starts from slightly left and up. 
        turtle.pendown()                #Put the pen down to draw the line from new position.

        #turtle.begin_fill()           (We can fill any color in the geometric pattern using this)
        #turtle.fillcolor("blue")      

        polygon(sides,length,depth)     #Calls the polygon function.
         #turtle.end_fill()              (Fills the color and ends)
                    
        turtle.done()                   #Finish the turtle program.
    
    
    except ValueError:             
        print("ERROR!!! Please enter valid input")

if __name__ == "__main__":       #Calling main function
   main()


   

                

                
            
            






