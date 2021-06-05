#!/usr/bin/python
# -*- coding: utf-8 -*-

##DEV##

# Any new command needs to be declared in the command list and added to the tinydic array

import os
import subprocess
import time
import datetime
from datetime import datetime
import sys
import requests
import json
import configparser
import getpass
import sqlite3
# Enable this in order to get Raspberry Pi Temp
#from gpiozero import CPUTemperature
#if os.system("uname -a | grep raspberry") == True:
#else:
#    pass

#Getting hostname
host = os.uname()[1]

#Getting username
user = getpass.getuser()


#Reading from the current path
path = __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Define your config, db and log file here
config_file = path+'/readMessages.conf'
#pathTodb = path+'/dbId.db'
pathTolog = path+'/readMessages.log'

#Database location
db = sqlite3.connect(path+'/readMessages.db')
cursor = db.cursor()

#Parsing config file
config = configparser.ConfigParser()
config.read(config_file)
apiKey = config['DEFAULT']['ApiKey']
apiKey_dev = config['DEFAULT']['ApiKey_DEV']
botchat = int(config['CHATS']['botchat'])
myid = int(config['USERS']['myid'])
alexid = int(config['USERS']['alexid'])
faid = int(config['USERS']['faid'])
btcholdings = float(config['CRYPTO']['btcholdings'])
ethholdings = float(config['CRYPTO']['ethholdings'])
ltcholdings = float(config['CRYPTO']['ltcholdings'])
xrpholdings = int(config['CRYPTO']['xrpholdings'])


#Whitelist
whitelist=[myid,faid,alexid]

#Misc Variables
log_time = datetime.now()


#Command List
ip = "/ip"
temp = "/temp"
all = "/all"
mycrypto = "/crypto"
mybtc = "/btc"
myeth = "/eth"
myltc = "/ltc"
myxrp = "/xrp"
help = "/help"
hitchhiker1 = "What's the meaning of life?"
hitchhiker2 = "What is the meaning of life?"

# If a command is not added here it will show as an error
tinydict = {ip,mycrypto,mybtc,myeth,myltc,myxrp,temp,help,hitchhiker1,hitchhiker2}

#Getting IP
#get_ip = requests.get('https://ipinfo.io/ip')


#GET JSON DATA from Telegram API - DEV
receive_data="https://api.telegram.org/bot"+str(apiKey_dev)+"/GetUpdates?offset=-1&limit=1"


#Messages
#ip_message = 'This is your ip: '+get_ip.text.strip('\n')

help_message = "I need somebody"

hitchhiker_message = "42"

error_message = "IP hasn't changed or the command is incorrect"

error_message2 = "Command not found"

error_message3 = "Trespassers will be shot, survivors will be shot again"

error_message4 = "Unable to provide the requested information"

# Variables for the Crypto Function
currentprice = 'https://www.bitstamp.net/api/v2/ticker/'


# Send function
def send():
    requests.post(bot_chat+message)



#Logging function
def writeLog():
    logFile = open(pathTolog,'a')
    logFile.write(str(text))
    logFile.write(os.linesep)
    logFile.write(str(log_time))
    logFile.write(os.linesep)
    logFile.write(str(json_data))
    logFile.write(os.linesep)
    logFile.close()


#Read DB function
def readDbFile():
    global pathTodb
    pathTodb = ''
    global dbFile
    dbFile = open(pathTodb,'r')
    global readlastline
    readlastline = dbFile.readline()
    dbFile.close()

#Write DB function
def writeDbFile():
    dbFile = open(pathTodb,'w')
    dbFile.write(str(message_id))
    dbFile.close()

#SQLITE FUNCTIONS

#Read from Sqlite DB
def getId():
    global lastid
    cursor.execute('SELECT messageid FROM messages order by date desc limit 1')
    lastid = cursor.fetchone()
    #print(int(lastid[0]))

#Write Sqlite DB
def writeId():
    cursor.execute('INSERT INTO messages(messageid, message, user, first_name, date) VALUES(?, ?, ?, ?, datetime())',(message_id, text, username, first_name, ))
    db.commit()


#Enable Logging
#logging = 'false'

#Enable verbose mode
verbose = 'true'


while True:
    
    try:
        new_request = requests.get(receive_data) 
        json_data = new_request.json()
    except requests.ConnectionError:
        pass

    
    
#Reading JSON Data
    try:
        text = json_data['result'][0]['message']['text'] # This gets the message
        message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
        userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
        username = json_data['result'][0]['message']['from']['username'] # This gets the username
        first_name = json_data['result'][0]['message']['chat']['first_name'] # This gets the first_name
        chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
    except KeyError: #This deals with the exceptions
        print(datetime.now())
        print("An Exception has ocurred, will keep going")
        pass

    #Read DB File
    #readDbFile()

    # Read from SQLITE DB
    getId()

    #Checking if message has been sent
    if int((lastid)[0]) == message_id:
        print("Checking SQLITE DB, Message has already been sent")
        #time.sleep(2)
    #Sending Messages 
        
    #Successful messages

    #Write DB File
    #writeDbFile()

    # Write to SQlite DB and close connection
    if message_id != int((lastid)[0]):
        writeId()
        print('Adding record to DB')
    else:
        print('Record already exists')

    #db.close()

    if verbose == "true":
        #print(json_data)
        #print(time)
        print(text)
        print(log_time)
        print("This is the message that we are getting from the JSON DATA: "+str(message_id))
        print("This is the last line that was written to the DB: "+str(lastid[0]))
        #print(userid)
        #print(new_id)
        #print (json.dumps(json_data,ensure_ascii=False,indent=2))

    #time.sleep(2)
    #break