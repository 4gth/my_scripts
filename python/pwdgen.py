import string
import argparse
import random

# Create arguments
parser = argparse.ArgumentParser(description = "Create strong passwords using a simple string builder")
parser.add_argument("-l", help="Set length of generated passwords", type=int) # sets option for length of password
parser.add_argument("-g", help="Set number of generated passwords", type=int) # sets option for how many passwords to generate
parser.add_argument("-s", help="Set use of symbols in generated passwords", action="store_true") # if used will generate passwords with symbols in .punctuation 
parser.add_argument("-n", help="Set use of numbers in generated passwords", action="store_true") # if used will generate passwords with numbers 0-9

args = parser.parse_args()

# Set variables to be used in main function, by default with no args passed will generate 1 password 8 characters long with no symbols or numbers
passwordLength = args.l or 8
numberOfPasswords = args.g or 1
includeSymbols = args.s
includeNumbers = args.n


# Main function that takes arguments and generates a string of random letters, numbers and symbols
def GeneratePassword(length, includeSymbols, includeNumbers):
    characters = string.ascii_letters
	
    if includeSymbols:
       characters += string.punctuation
		
    if includeNumbers:
        characters += string.digits

    password = ''.join(random.choice(characters) for _ in range (length))
    return password

# calls GeneratePassword function as many times as required by the -g argument
passwords = '\n'.join(GeneratePassword(passwordLength, includeSymbols, includeNumbers) for _ in range(numberOfPasswords))


print(passwords)
