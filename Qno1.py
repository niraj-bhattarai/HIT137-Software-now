"Encryption and decryption"


#importing os :to work with the current directory
import os

""" Note :The inital idea of this code was inspired by 

# ChatGPT (OpenAI) suggested using modulo % 26 for Caesar cipher wrap-around. 
    .accessed on Aug 27 2025
# This avoids manual if-checks and works for large shifts
chr(((ord(ch) - ord('a') + shift) % 13) + ord('a')) this"""



#i have used mode 13 because it helps to keep the characters witin in range as there are differenent cases for encryption for different range of alphabets



#defining the main function 
def main():


    #the number of shift asked to the user 
    try:
        shift1=int(input("Enter the first shift number : "))
        shift2=int(input("Enter the second shift number : "))

    except ValueError:
        print("The shift value must be in integer ie 1,2,3")




    #calling the encryption function
    encryption(shift1,shift2)
    #callinf the decryption function
    decryption(shift1,shift2)
    #calling the varification funciton
    verfication()

    



    
   

   


   


def verfication():
    #getting the current working directory
    path=os.getcwd()

    #opened mutiple file at once
    with open(path + "\\decrypted_text.txt", "r") as decrypted_txt, \
         open(path + "\\raw_text.txt", "r") as raw_txt:
        
        if decrypted_txt.read() == raw_txt.read():
            print("The decryption was successful")
        else:
            print("Decryption failed")
        

#function to decrypt the text
def decryption(shift1,shift2):
    #getting the path for current working directory
    path=os.getcwd()

    #opening the encrypted_txt.txt from the directory
    with open(path+"\\encrypted_text.txt","r") as encrypted_text:
        input_encrypted_text=encrypted_text.read()
        encrypted_text.close()
    

    #inilized the decrypted_text
    decrypted_text=""


    #loop thorugh every chracter
    for ch in input_encrypted_text:
          #checking condition for the lower case
          if ch.islower():
              #condtion for the range a to m  mode 13 because it range 13 characters
              if 'a' <= ch <= 'm':
               
                shift = (shift1 * shift2) % 13
                decrypted_text += chr(((ord(ch) - ord('a') - shift) % 13) + ord('a'))
            
              else:
                shift = (shift1 + shift2) % 13
            
                decrypted_text += chr(((ord(ch) - ord('n') + shift) % 13) + ord('n'))

          elif ch.isupper():
              #condtion for the A to M  
              if 'A' <= ch <= 'M':
            
                shift = (shift1 % 13)
                decrypted_text += chr(((ord(ch) - ord('A') + shift) % 13) + ord('A'))
              else:
                #accorf
                shift = (shift2**2) % 13
                decrypted_text += chr(((ord(ch) - ord('N') - shift) % 13) + ord('N'))

          else:
              #No change for the remaining
              decrypted_text += ch
    


    #opening and writing the decrypted content to the result
    with open("decrypted_txt.txt","w") as decryption_result:
        decryption_result.write(decrypted_text)




#funciton to handle the encryption 
def encryption(shift1,shift2):
    #getting the current working directory using the OS (built-in library)
    path=os.getcwd()


    #need to remove just for testing
    print(path)

    #opening the file from the current directory
    #need to handle excepption gracefully :what if there is no file named raw.txt
    with open(path+"\\raw_text.txt","r") as plain_text:
        #reading the text from the file
        input_plain_text=plain_text.read()
        #closing the file
        plain_text.close()

    #setting the empty string to append 
    cipher_text=""

    #looping through each character
    for ch in input_plain_text:
        
        #checking if the character is lower or not
        if ch.islower():
            """ checking the conditions accrording to the questions 
            range a to m """
            if 'a'<= ch <='m':
                #making the base upto 13 charcter ie :using mode 13 
                shift = (shift1*shift2) % 13
                cipher_text += chr(((ord(ch) - ord('a') + shift) % 13) + ord('a'))
            #for the other range  n to z
            else:
                #making the base upto 13 charcter ie :using mode 13 
                shift = ((-(shift1+shift2)) % 13)
                cipher_text += chr(((ord(ch) - ord('n') + shift) % 13) + ord('n'))
        
        #condition for the upper case
        elif ch.isupper():
            if 'A' <=ch <= 'M':
                # FIX: keep inside A..M (13 letters). Use base 'A' and %13.
                shift = ((-shift1) % 13)
                cipher_text += chr(((ord(ch) - ord('A') + shift) % 13) + ord('A'))
            else:
                # FIX: keep inside N..Z (13 letters). Use base 'N' and %13.
                shift = ((shift2**2) % 13)
                cipher_text += chr(((ord(ch) - ord('N') + shift) % 13) + ord('N'))
        else:
            cipher_text+=ch


    #creating and opening the encrypted_txt.txt for encrypted text
    with open("encrypted_txt.txt","w") as encrypted:
        encrypted.write(cipher_text)
        encrypted.close() 

    


            

          
           






#calling the main function 
if __name__ == "__main__":
    main()

