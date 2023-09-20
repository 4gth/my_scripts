import json




logfile = open('db_silca_log.log', 'w')

#Load the input .json file thats been cleaned
with open('db_silca_log.json') as file:
    loadedJson = json.load(file)


for keys in loadedJson:
    log = keys['log']
    logfile.write(log)
    print(log)