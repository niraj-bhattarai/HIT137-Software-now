"Encryption and decryption"


#importing os :to work with the current directory
import os

""" Note :The inital idea of this code was inspired by 

# ChatGPT (OpenAI) suggested using modulo % 26 for Caesar cipher wrap-around. 
    .accessed on Aug 27 2025
# This avoids manual if-checks and works for large shifts
return chr((ord(ch) - ord('A') + shift) % 26 + ord('A')) this"""



#defining the main function 
def main():


    #the number of shift asked to the user 
    shift1=int(input("Enter the first shift number : "))
    shift2=int(input("Enter the second shift number : "))

    #getting the current working directory using the OS (built-in library)
    path=os.getcwd()
    print(path)



    
    #initilizing the variable encrypted_text
    encrypted_text=""

   


    #opening the file from the current directory
    #need to handle excepption gracefully :what if there is no file named raw.txt
    with open(path+"\\raw_text.txt","r") as plain_text:
        #reading the text from the file
        input_plain_text=plain_text.read()



        encrypted_text=encryption(input_plain_text,shift1,shift2)

        #closing the file
        plain_text.close()



       
    with open("encrypted_txt.txt","w") as encrypted:
        encrypted.write(encrypted_text)
        encrypted.close()
    


    #testing for now Nedd to remove for the final version
    print("the decrypted text is",decryption(encrypted_text,shift1,shift2))





#function to decrypt the text
def decryption(encrypted_text,shift1,shift2):
    #inilized the decrypted_text
    decrypted_text=""
    #loop thorugh every chracter
    for ch in encrypted_text:
          #checking condition for the lower case
          if ch.islower():
              #condtion for the range a to m
              if 'a' <= ch <= 'm':
                shift = -(shift1 * shift2)
                decrypted_text+= chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
                #condtion for n to z
              else:
                shift = (shift1 + shift2)
                decrypted_text += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
          elif ch.isupper():
              #condtion for the A to M
              if 'A' <= ch <= 'M':
                shift = shift1
                decrypted_text += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
              else:
                #Condition for N to Z

                shift = -(shift1 ** 2)
                decrypted_text += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
    else:
        #No change for the remaining
        decrypted_text += ch
  
    #returning the decrypted text
    return decrypted_text

#funciton to handle the encryption 
def encryption(plain_text,shift1,shift2):
    #setting the empty string to append 
    cipher_text=""


    #looping through each character
    for ch in plain_text:
        
        
        #checking if the character is lower or not
        if ch.islower():
            """ checking the conditions accrording to the questions 
            range a to m """
            if 'a'<= ch <='m':
                shift=shift1*shift2
                
                cipher_text+= chr((ord(ch)-ord ('a')+shift)%26 +ord ('a'))
            #for the other range  n to z
            else:
                shift=-(shift1+shift2)
                cipher_text+= chr((ord(ch) -ord('a')+shift) %26 +ord('a'))
            
            
        
        #condition for the upper case
        elif ch.isupper():
            if 'A' <=ch <= 'M':
                shift= -shift1
                cipher_text+=chr(ord(ch) - ord('A') + shift) % 26 + ord('A')
            else:
                shift= shift1**2 
                cipher_text+= chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        else:
         cipher_text+=ch 
    return cipher_text


            

          
           






#calling the main function 
if __name__ == "__main__":
    main()

