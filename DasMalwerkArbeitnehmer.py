'''
DasMalwerkArbeitnehmer by @sk3tchymoos3
Version 1.0 -> outputs list to csv and can also search and download by SHA256
'''

import requests
import json
import argparse
import sys
import csv

# START FUNCTIONS

def gebenDasFile():
    r = requests.get('http://dasmalwerk.eu/api')
    if (r.status_code == requests.codes.ok):
        pass
    else:
        print "Das malwerk ist mude... Versuchen Sie es spaeter noch einmal!"
        exit()
    data = json.loads(r.text)
    return data

def allesMalwerk(data):
    f = open('allesMalwerk.csv','wb')
    csvwriter=csv.writer(f)
    counter = 0
    for dataitems in data["items"]:
        if counter == 0:
            header = dataitems.keys()
            csvwriter.writerow(header)
        counter = counter + 1
        csvwriter.writerow(dataitems.values())
        for key, value in dataitems.iteritems():
            print key, "is:", value
        print ''
    print "Parsed %d items in the zoo" % counter
    print "Check current directory for CSV output!"
    f.close()

def suchenMalwerk(data, SHA256hash):
    for dataitems in data["items"]:
        for key, value in dataitems.iteritems():
            if key == "Hashvalue":
                if value == SHA256hash:
                    print "Hash found!"
                    malwerkfilename=dataitems["Filename"]
                    herunterladen(malwerkfilename)
                    print "File downloaded to current directory, password is infected"
                    VTLink=dataitems["Moreinformation"]
                    print "Get more info here: ", VTLink
                else:
                    break

def herunterladen(malwerkfilename):
    malwerkfilename=str(malwerkfilename) + ".zip"
    urlfurherunterladen="http://dasmalwerk.eu/zippedMalware/"+ malwerkfilename
    tofile = requests.get(urlfurherunterladen,stream=True)
    with open(malwerkfilename, "wb") as code:
        for chunk in tofile.iter_content(1024):
            code.write(chunk)

#START CODE

parser = argparse.ArgumentParser(description='Ich bin ein Malware jaeger!')
parser.add_argument('-s', '--search', help='Search & Download a particular SHA256 if available')
parser.add_argument('-l','--list' ,help='List all the files', action='store_true')

data=gebenDasFile()

args = vars(parser.parse_args())

if len(sys.argv) < 2:
    print "Need an argument"
    parser.print_help()
    exit()
if args['list']:
    allesMalwerk(data)
if args['search']:
    SHA256hash = args['search']
    suchenMalwerk(data, SHA256hash)







