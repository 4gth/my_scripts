# This script takes a targetFile, calculates its checksum(calculate_checksum) using hashlib Md5.
# After this it iterates through each other file in the directory ignoring other folders.
# Using the same calculate_checksum function it calculates its checksum
# It then compares it to the targetFile. If the checksum is the same it prints a line to let you know

import hashlib
import os

def calculate_checksum(filePath): # Main function for creating checksums for files
    hashMD5 = hashlib.md5()
    with open(filePath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hashMD5.update(chunk)
        return hashMD5.hexdigest()

def main():
    targetFile = 'Toyota 89666-06440 93c56 Central Victorian LS.bin' # Change to target file #TODO add args
    directory = '.' #runs in script directory

    targetChecksum =  calculate_checksum(targetFile)

    for entry in os.listdir(directory):         # Main function for comparing checksum to checksums of all other files in directoy
        filePath = os.path.join(directory, entry)
        if os.path.isfile(filePath) and entry != targetFile:
            checksum = calculate_checksum(entry)
            if checksum == targetChecksum:
                print(f'\033[93m' + f'Dupe found:' + f'\033[0m' f'{entry}' + f'\033[93m' ' and ' + f'\033[0m' f'{targetFile}')


if __name__ == '__main__':
    main()