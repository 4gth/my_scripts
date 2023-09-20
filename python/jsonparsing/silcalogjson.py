

# This is bad was put together while learning to deal with json key:values
# I was in a rush to get the info out of the logs


import json



#open log3 log 1 and logkeys files with write permissions
log3 = open('log3.log', 'w')
log1 = open('log1.log', 'w')
logkeys = open('logkeys.log', 'w')

#Load the input .json file thats been cleaned
with open('applog.json') as f:

    loadedJson = json.load(f)


#Start parsing through json file

for keys in loadedJson:                 #top level
    
    if keys['log_level'] == 1 and 'message' in keys: #the return on this is kinda useless
        log1.write(f'''
timestamp: {keys['timestamp']}
log_level: {keys['log_level']}
message: {keys['message']}

''')
    
    if keys['log_level'] == 3:
       log3.write(f'''
timestamp: {keys['timestamp']}
log_level: {keys['log_level']}
event: {keys['event']}''')
    
    meta = [keys['meta_data']]  #access to meta_data nested lists/dictionaries
    for subkey in meta:
        if 'id' in subkey:      #make formatted strings to write to log3
            log3.write(f''' 
id: {subkey['id']}
board: {subkey['board']}
''')
        
        elif 'message' in subkey: #more stuff to add to log3 string if availible
            log3.write(f'''
message: {subkey['message']}
route: {subkey['route']}
''')
            
   

for keys in loadedJson:           #back to top level
    meta = [keys['meta_data']]
    for subkey in meta:           #Jump to meta_data
        if 'job' in subkey:       #Jump to job list
               #String formatter for dumping log of all keys cut that were sent to SSI queue....super secure guys.
            if 'type' in subkey['job'] and 'engraving' in subkey['job'] and 'customer' in subkey['job']:
                customername = subkey['job']['customer']
                keyprofile = subkey['job']['engraving']['name']
                keyrank = subkey['job']['cipher']['code']
                keycuts = subkey['job']['cipher']['cuttings'].replace(';', '')
                    
                logkeys.write(customername + ' ---> ' + keyprofile + ' ---> ' + keyrank + ' ---> ' + keycuts + '\n')
        

 #Close 
log1.close()
log3.close()
logkeys.close()