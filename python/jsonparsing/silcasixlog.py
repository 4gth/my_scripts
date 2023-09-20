# This script is used for quickly dumping Silca's machine logs from he Unocode F platform.
# The machine consists of a bunch of Docker containers running various databases, HTTP webservers, and customer apps.

# The script will deals with 2 types of logs, both types are Json. getdockerlog() will simply dump log events to file.
# it takes 2 arguments technically, but there's nothing interesting aside from ['log'] so just pass it -l <dockerlog.json> -k log

# sixlogwriter() takes only 1 argument which is path to .json -s </application_log.sixlog> 
# and will specifically write to file(csv) all keys that were sent to SSI queue
# this contains this includes[timestamp, customer name, key profile, key rank, key cuts, qty keys cut]


# Author Justin Manners 2023, no copyright - this code probably is no good.

import json
import csv
import argparse

argument = argparse.ArgumentParser(description = 'script for decoding Silca "SixPC" logs') # Setting up args
argument.add_argument('-s', help = 'path to application_log.sixlog.json file')             # so we can run on other files
argument.add_argument('-l', help = ' path to docker.json.log file')                        # json files should be cleaned using
argument.add_argument('-k', help = 'key to seach docker log json recommend only "log"')    # some regex and jq, the logs don't
args = argument.parse_args()                                                               # dump to the USB correctly it seems

sixlog = args.s               # The sixlog is found in /tmp/log/application_log.sixlog.gz
dockerlog = args.l            # All docker logs are found in /tmp/log/docker 
key = args.k                  # Just use log, its here incase I decide to expand

def sixlogwriter(getfile):    # Main function for .sixlog file


    with open(getfile) as f:
        loadedJson = json.load(f)                   # Create dictionary from input json file
    csvf = open(f'{getfile}.keys.csv', 'x')        
    csvwriter = csv.writer(csvf, delimiter=',')     # Create csvwriter object for writing to csv file
    for keys in loadedJson:
                                                    # Main loop for entering each key: tree to see if our target keys are there
        if 'job' in keys['meta_data'] and 'cipher' in keys['meta_data']['job'] and 'engraving' in keys['meta_data']['job']:
            timestamp = keys['timestamp']                                                   # Bunch of variables for our data
            customer = keys['meta_data']['job']['customer']                                 # There are so many more keys in
            keyname = keys['meta_data']['job']['cipher']['key_name']                        # in this file you could pull so
            keycuts = keys['meta_data']['job']['cipher']['cuttings'].replace(';' , '')      # much more out of it. 
            qty = keys['meta_data']['job']['cipher']['quantity']                            # Spare time project.
            keyprofile = keys['meta_data']['job']['engraving']['name']                      # TODO add ability to search for key:
            print(f'{customer}, {keyprofile}, {keyname}, {keycuts}, {qty}')
            csvwriter.writerow([timestamp, customer, keyprofile, keyname, keycuts, qty])    # Write :values to csv file
    csvf.close()

def logwriter(getdockerlog, getkey): # Main function for dropping 'log keys from dockerlogs
    with open(getdockerlog) as f:
        dockerlogload = json.load(f)                # Create dictionary from input json
    logwrite = open(f'{getdockerlog}.log', 'x')     # Create writer object for writing to .log file
    for keys in dockerlogload:                      # Main loop looking for key: and writing to .log file
        print(keys[getkey])
        logwrite.write(keys[getkey])

# if statements to check args and run appropiate function
if sixlog: sixlogwriter(sixlog)
if dockerlog: logwriter(dockerlog, key)
