"Encryption and decryption"


#importing os :to work with the current directory
import os

""" Note :The inital idea of this code was inspired by 

# ChatGPT (OpenAI) suggested using modulo % 13 for Caesar cipher wrap-around. 
    .accessed on Aug 27 2025
# This avoids manual if-checks and works for large shifts
chr(((ord(ch) - ord('a') + shift) % 13) + ord('a')) this"""



#i have used mode 13 because it helps to keep the characters witin in range as there are differenent cases for encryption for different range of alphabets

"""try ane except has been implemented through out the code 
Exception is being used rather than specific error because it accomodates a lot of errors at once ranther than addressing
individual kind of error in order to reduce the code complication """


#defining the main function 
def main():
  #the number of shift asked to the user 
    try:
        shift1=int(input("Enter the first shift number : "))
        shift2=int(input("Enter the second shift number : "))

    except ValueError:
        print("The shift value must be in integer ie 1,2,3")


    #getting the current working directory
    #initilizing the path value as it is required so i updated this to reduce the redundency
    path=""
    try:
        path=os.getcwd()
    except Exception as e:
        #printing this error makes it easier to see the problem
        print("Error getting the path ",e)



    try:
        #calling the encryption function
        encryption(path,shift1,shift2)
        #callinf the decryption function
        decryption(path,shift1,shift2)
        #calling the varification funciton
        verfication(path)
    except Exception as e:
        print("Error completing the steps",e)

    
    


   


def verfication(path):
   
    
    #opened mutiple file at once the \ separetes the line 
    try:
        with open(path + "\\decrypted_text.txt", "r") as decrypted_txt, \
         open(path + "\\raw_text.txt", "r") as raw_txt:
            #comparing the two files according to the quesetion
            if decrypted_txt.read() == raw_txt.read():
                print("The decryption was successful")
            else:
                print("Decryption failed")
    except Exception as e:
        print("Error occured while accessing the file during verification ",e)

        
#function to decrypt the text
def decryption(path,shift1,shift2):
    #opening the encrypted_txt.txt from the directory
    try:
        with open(path+"\\encrypted_text.txt","r") as encrypted_text:
            input_encrypted_text=encrypted_text.read()
            encrypted_text.close()
    

    except Exception as e:
        print("Error occured opening encrypted_text",e)
    

    #inilized the decrypted_text
    decrypted_text=""


    #loop thorugh every chracter
    for ch in input_encrypted_text:
          #checking condition for the lower case
          if ch.islower():
              #condtion for the range a to m  mode 13 because it range 13 characters
              if 'a' <= ch <= 'm':

               #condition according to question and mode 13 to wrap around the  13-letters
                shift = (shift1 * shift2) % 13

                # Decodes a single character by shifting its ASCII code backwards within the range 'a'–'m',
                # wrapping around using modulo arithmetic to ensure the result stays in this 13-letter block.
                decrypted_text += chr(((ord(ch) - ord('a') - shift) % 13) + ord('a'))
            
              else:
                #condition according to question and mode 13 to wrap around the  13 alphabets
                shift = (shift1 + shift2) % 13
                decrypted_text += chr(((ord(ch) - ord('n') + shift) % 13) + ord('n'))

          elif ch.isupper():
              #condtion for the A to M  
              if 'A' <= ch <= 'M':
                #condition according to question and mode 13 to wrap around the  13 alphabets
                shift = (shift1 % 13)
                decrypted_text += chr(((ord(ch) - ord('A') + shift) % 13) + ord('A'))
              else:
                #condition according to question and mode 13 to wrap around the  13 alphabets
                shift = (shift2**2) % 13
                decrypted_text += chr(((ord(ch) - ord('N') - shift) % 13) + ord('N'))

          else:
              #No change for the remaining
              decrypted_text += ch
    


    #opening and writing the decrypted content to the 
    try:
        with open("decrypted_text.txt","w") as decryption_result:
            decryption_result.write(decrypted_text)
            decryption_result.close()
    except Exception as e:
        print("Error occured in writing decrypted.txt",e)




#funciton to handle the encryption 
def encryption(path,shift1,shift2):
    #opening the file from the current directory
    #need to handle excepption gracefully :what if there is no file named raw.txt
    try:
        with open(path+"\\raw_text.txt","r") as plain_text:
            #reading the text from the file
            input_plain_text=plain_text.read()
            #closing the file
            plain_text.close()
    except Exception as e :
        print("Error occured in opening the raw text in encryption",e)


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
                #making base 13
                shift = ((-shift1) % 13)
                cipher_text += chr(((ord(ch) - ord('A') + shift) % 13) + ord('A'))
            else:
                #making base 13
                shift = ((shift2**2) % 13)
                cipher_text += chr(((ord(ch) - ord('N') + shift) % 13) + ord('N'))
        else:
            cipher_text+=ch


    #creating and opening the encrypted_txt.txt for encrypted text
    try:
        with open("encrypted_text.txt","w") as encrypted:
            encrypted.write(cipher_text)
            encrypted.close() 
    except Exception as e:
        print("Error occured in writing the encrypted_text",e)

    


            

          
           






#calling the main function 
if __name__ == "__main__":
    main()

