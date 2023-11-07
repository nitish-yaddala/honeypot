# Monitoring script
import os 
import json
import requests
import time

LOGS_FOLDER = "./logs"
URL ="http://127.0.0.1:5001/honeypotlogs"
FTP_LOGCOUNT =0
SSH_LOGCOUNT=0


logs_list = os.listdir(LOGS_FOLDER)


def sendlogs():
    global SSH_LOGCOUNT
    global FTP_LOGCOUNT
    print("\n Monitoring Script \n")
    for filename in logs_list:
        file = open(f"{LOGS_FOLDER}/{filename}").readlines()
        temp_file = dict()
        if (filename=="ftp.log" and len(file)> FTP_LOGCOUNT):
            temp_file= file[FTP_LOGCOUNT:]
            FTP_LOGCOUNT= len(file)
        elif (filename=="ssh.log" and len(file)> SSH_LOGCOUNT):
            temp_file= file[SSH_LOGCOUNT:]
            SSH_LOGCOUNT= len(file)
        final_dicts = [json.loads(y.strip()) for y in temp_file if 'error' not in y]
        for single_dict in final_dicts:
            response = requests.post(URL, json=single_dict)
            print(response.text)

while True:
    sendlogs()
    time.sleep(5)