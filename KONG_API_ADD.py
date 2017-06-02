import argparse
import csv
import requests
import copy
import json
import sys
import time
import os
import urllib3
import certifi
urllib3.disable_warnings()
https = urllib3.PoolManager(
     cert_reqs='CERT_REQUIRED',
     ca_certs=certifi.where())


# DEV env
KONG_API_END_POINT = "http://128.199.67.132:8001/apis/"

#USER = "sreemanth"
#PASSWORD = "dHZnYlBodzZ5Vg=="

#CSV COLUMN NO
API_NAME_NO=0
HOST_NAME_NO=1
UPSTREAM_URL_NO=2

#HEADER
HEADER = {'content-type':'application/json'}

#BODY
API_ADD_REQUESTS = { 
  "name": "test-ccd-api2",
  "hosts": "test-lapp-api.fourthlion.in",
  "upstream_url" : "https://139.59.242.244"
}

def add_apis_to_server(input_file, no_of_lines_to_skip):
    print("Input file", input_file)
    with open(input_file, "r") as infile:
        rows = csv.reader(infile)
        # skip headers lines
        for i in range(no_of_lines_to_skip):
            next(rows)
        # process
        for row in rows:
            try:
                API_ADD_REQUESTS['name'] = row[API_NAME_NO].strip()
                API_ADD_REQUESTS['hosts'] = row[HOST_NAME_NO].strip()
                API_ADD_REQUESTS['upstream_url'] = row[UPSTREAM_URL_NO].strip() 
                # Send to serve
                print(API_ADD_REQUESTS)
                #HEADER['From'] = USER
                #HEADER['Authorization'] = PASSWORD
                response = requests.post(KONG_API_END_POINT, headers=HEADER, data=json.dumps(copy.deepcopy(API_ADD_REQUESTS)))
                print(response.text)
                print(response.status_code)
                print(response.reason)
            except:
                e = sys.exc_info()
                print("Error: ", e)
            time.sleep(1)
                
    
                

"""
    Add APIs to Server
    -----------------------------------
    python3 KONG_API_ADD.py -a addApis -i apis.csv
    
"""
            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser("add apis")
    parser.add_argument("-a", "--action", required=True)
    parser.add_argument("-i", "--inputfile")
    parser.add_argument("-n", "--nooflines", type=int, default=1)
    
    args = parser.parse_args()
    if args.action == "addApis":
        add_apis_to_server(args.inputfile, args.nooflines)
