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
password_length = args.l or 8
number_of_passwords = args.g or 1
include_symbols = args.s
include_numbers = args.n


# Main function that takes arguments and generates a string of random letters, numbers and symbols
def generate_password(length, include_symbols, include_numbers):
    characters = string.ascii_letters
	
    if include_symbols:
       characters += string.punctuation
		
    if include_numbers:
        characters += string.digits

    password = ''.join(random.choice(characters) for _ in range (length))
    return password

# calls generate_password function as many times as required by the -g argument
passwords = '\n'.join(generate_password(password_length, include_symbols, include_numbers) for _ in range(number_of_passwords))


print(passwords)
