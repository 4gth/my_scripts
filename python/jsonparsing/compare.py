import csv

with open('phonenumbers.txt', 'r') as txtfile:
    txtreader = []
    for i in txtfile:
        txtreader.append(txtfile.readline().strip().split(','))

print(type(txtreader))
print(txtreader)

for i in txtreader:
    if len(i) == 2:
        i.insert(1, " ")
"""
print(txtreader)

with open ("cleanedphonenumbers.csv") as csvfile:
    phonewriter = csv.writer(csvfile, delimiter= ' ')
    for j in txtreader:
        phone = j[2]
        acc = j[1]
        name = j[0]
        print(name,acc,phone)
        phonewriter.writerow([2][1][0])
"""










"""
with open('phonenumbers.csv', 'w',newline='') as csvfile:
    
    phonewriter = csv.writer(csvfile, delimiter=',')
    phonewriter.writerow(['phone'])
    for i in txtreader:
       phonewriter.writerow([txtreader[i]])
"""

"""
with open('contactsexport.csv', 'r') as contactsCSV:
    contactReader = csv.DictReader(contactsCSV)

    for row in contactReader:
        phone = row["phone"]
        acc = row["acc"]
        name = row["name"]     
        for numbers in txtreader:
            if phone == numbers:
                print("found:", phone, acc, name)
            
                
   """                 

        