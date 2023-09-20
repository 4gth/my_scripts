# This script takes a CSV file with [phone, account #, name] fields
# it then places them in a large string along with a UUID
# All for the sake of being able to import phone numbers from Epicor or scraped from other peoples contacts.dat file 

# The first entry in the new contacts.dat file needs to be in a 'Group' all other contacts must have the same $ref
# "Groups": [
#       {
#         "$id": "1",
#         "$type": "Mitel.Communicator.Models.ContactGroup, Mitel.Communicator.Models",
#         "GroupType": 1,
#         "ID": "1341",
#         "IsExpanded": true,
#         "Name": "Customer",
#         "Order": 3
#      }
#     ],
# "Groups": [
#       {
#        "$ref": "1",
#       }
#     ],

import csv
import json
import uuid

def generatejsonfromCSV(csv_filepath, json_filepath):
	json_data = []										# Empty list, we will write this to .json file at the end
	with open(csv_filepath, 'r') as csv_file:			# CSV reader object so we can pull our variables from the phone book
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:							# Main loop to reads each line grabs each field
			phone = row["phone"]						# passes them to a variable
			acc = row["acc"]
			name = row["name"]
			unique_id = str(uuid.uuid4())
			

			data = {			# Main entry for our new contact, adds variables to where ever we need it.
			 
   				"$type": "Mitel.Communicator.Models.Contact, Mitel.Communicator.Models",
				"ID": unique_id,
				"UUID": unique_id,
				"ContactType": 2,
				"FirstName": name,
				"LastName": acc,
				"MiddleName": "",
				"LogName": name,
				"Address": "",
				"ForeignKey": "",
				"CompanyName": "",
				"Phones": [
				{
					"$type": "Mitel.Communicator.Models.Phone, Mitel.Communicator.Models",
					"ID": -1,
					"Label": "Phone",
					"Number": phone,
					"DeviceTypes": [],
					"ContactType": 2,
					"Detail": {
					"$type": "Mitel.Communicator.Models.PhoneDetail, Mitel.Communicator.Models",
					"PhoneContext": "",
					"Extension": "",
					"Parameters": {
						"$type": "System.Collections.Hashtable, mscorlib"
					}
					},
					"IsDefault": True
				}
				],
				"Emails": [],
				"Messengers": [],
				"AccountId": -1,
				"PictureURL": "",
				"Groups": [
				{
					"$ref": "3"					# Change this to suit
				}
				],
				"DefaultPhoneNumber": phone,
				"SearchableAttributes": []
  
		}
			json_data.append(data) 				# Adds this data to our json list
			

	with open(json_filepath, 'w') as json_file:		# After main loop ends, create json writer object and .dump it to file
		json.dump(json_data, json_file, indent=2)

if __name__ == "__main__":							# Call main function
	csv_filepath = "contactsexport.csv"				# TODO: add args
	json_filepath = "contactsexport.json"
	generatejsonfromCSV(csv_filepath, json_filepath)
