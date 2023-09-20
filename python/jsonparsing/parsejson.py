

# Hacky script when I first looked at parsing json
# Script will loop through .json file looking for 'phones and 'LogNames' in a Mitel formatted contacts.dat file
#TODO The entire thing again


import json
import csv

inputFile = open('contactswill.dat', 'r')
List = json.loads(inputFile.read())
f = open("phonenumbers.txt", "a")
g = open("LogName.txt", "a")
print(type(List))
for i in range(len(List)):
    Phones = List[i]["Phones"]
    LogName = List[i]["LogName"]
    for j in range(len(Phones)):
        Number = Phones[j]["Number"]

        f.write(LogName + "," + Number + "\n")
        print(Number)
"""
for i in range(len(List)):
    LogName = List[i]["LogName"]
    g.write(LogName + '\n')
"""


f.close()
inputFile.close()