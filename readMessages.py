#!/usr/bin/python
# -*- coding: utf-8 -*-

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

#Getting hostname
host = os.uname()[1]

#Getting username
user = getpass.getuser()

#Reading from the current path
path = __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Define your config, db and log file here
config_file = path+'/readMessages.conf'
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

#Misc Variables


#GET JSON DATA from Telegram API - DEV
receive_data="https://api.telegram.org/bot"+str(apiKey_dev)+"/GetUpdates?offset=-1&limit=1"


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


#SQLITE FUNCTIONS
#Read from Sqlite DB
def getId():
    global lastid
    cursor.execute('SELECT messageid FROM messages order by date desc limit 1')
    lastid = cursor.fetchone()
    #print(int(lastid[0]))

#Write Sqlite DB
def writeId():
    cursor.execute('INSERT INTO messages(messageid, message, user, firstname, chatname, date) VALUES(?, ?, ?, ?, ?, datetime())',(message_id, text, username, first_name, chatName, ))
    db.commit()

#Update functions below
def updateEditedflag():
    cursor.execute('UPDATE messages set edited = ?, updateddate = ?', (edited, editedMsgdate,))
    db.commit()

def updateMsg():
    cursor.execute('SELECT messageid, message FROM messages where messageid = ?', (editedMsgId,))
    origMsg = cursor.fetchone()
    cursor.execute('INSERT INTO updatedmessages(messageid, originalmessage, updatedmessage, updateddate, date) VALUES(?,?,?,?,datetime())' ,(origMsg[0], origMsg[1], editedMsg, editedMsgdate,))
    db.commit()

def updateMsgagain():
    cursor.execute('UPDATE updatedmessages set updatedmessage = ?, updateddate = ?, date = datetime() where messageid = ?', (editedMsg, editedMsgdate, editedMsgId,))
    db.commit()

def getUpdateddate():
    global lastupdate
    cursor.execute('SELECT updateddate FROM updatedmessages where messageid = ?', (editedMsgId,))
    lastupdate = cursor.fetchone()

def checkIfupdated():
    cursor.execute('SELECT updateddate FROM messages WHERE messageid = ?', (editedMsgId,))
    global updated_date
    updated_date = cursor.fetchone()




#Enable Logging
#logging = 'false'

#Enable verbose mode
verbose = 'true'

while True:

    log_time = datetime.now()
    
    try:
        new_request = requests.get(receive_data) 
        json_data = new_request.json()
    except requests.ConnectionError:
        pass

    editedMsgId = None
    message_id = None
    username = None
    #editedMsg = None
    #editedMsgdate = None
    #text = None
    #userid = None
    #username = None
    #first_name = None
    #chatid = None
    #chatName = None

    
    # This deals with normal messages in group chats
    if 'message' in json_data['result'][0] and json_data['result'][0]['message']['chat']['type'] == 'group':
        print('This is anything in a group')
        if 'text' in json_data['result'][0]['message'] and 'username' in json_data['result'][0]['message']['from']:
            print('This is a message')
            text = json_data['result'][0]['message']['text'] # This gets the message
            message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
            userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
            username = json_data['result'][0]['message']['from']['username'] # This gets the username
            first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
            chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
            chatName = json_data['result'][0]['message']['chat']['title'] # This gets the chat Name
        elif 'text' in json_data['result'][0]['message']:
            print('This is a message')
            text = json_data['result'][0]['message']['text'] # This gets the message
            message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
            userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
            first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
            chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
            chatName = json_data['result'][0]['message']['chat']['title'] # This gets the chat Name
        else:
            print('Whatever this is, I dont care for it')

    # This deals with edited messages in group chats
    elif 'edited_message' in json_data['result'][0] and json_data['result'][0]['edited_message']['chat']['type'] == 'group':
        print('This is anything edited in a group')
        if 'text' in json_data['result'][0]['edited_message']:
            print('This is an edited message')
            editedMsg = json_data['result'][0]['edited_message']['text'] # This gets the edited message text 
            editedMsgId = json_data['result'][0]['edited_message']['message_id'] # This gets the edited message ID
            editedMsgdate = json_data['result'][0]['edited_message']['edit_date'] # This gets the edited message date
            date = json_data['result'][0]['edited_message']['date'] # This gets the original message date
        else:
            print('Whatever this is, I dont care for it')

    # This deals with normal messages in private chats
    elif 'message' in json_data['result'][0] and json_data['result'][0]['message']['chat']['type'] == 'private':
        print('This is anything in a private chat')
        if 'text' in json_data['result'][0]['message']:
            print('This is a message')
            text = json_data['result'][0]['message']['text'] # This gets the message
            message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
            userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
            username = json_data['result'][0]['message']['from']['username'] # This gets the username
            first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
            chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
        else:
            print('Whatever this is, I dont care for it')

    # This deals with edited messages in private chats
    elif 'edited_message' in json_data['result'][0] and json_data['result'][0]['edited_message']['chat']['type'] == 'private':
        print('This is anything edited in a private chat')
        if 'text' in json_data['result'][0]['edited_message']:
            print('This is an edited message')
            editedMsg = json_data['result'][0]['edited_message']['text'] # This gets the edited message text 
            editedMsgId = json_data['result'][0]['edited_message']['message_id'] # This gets the edited message ID
            editedMsgdate = json_data['result'][0]['edited_message']['edit_date'] # This gets the edited message date
            date = json_data['result'][0]['edited_message']['date'] # This gets the original message date
        else:
            print('Whatever this is, I dont care for it')
    
    else:
        print('This is other type of message')


    # Read from SQLITE DB
    getId()

    # Check Edited message date
    checkIfupdated()

    # Check if the date in the updated messages table has changed
    getUpdateddate()    

    
    # Write to SQlite DB and close connection
    if message_id != None and message_id != int((lastid)[0]):
        writeId()
        print('Adding record to DB')
    elif editedMsgId != None and editedMsgId == int((lastid)[0]) and editedMsgdate != (updated_date[0]):
        edited = 1
        if updated_date[0] == None:
            print('Updating Message')
            updateMsg()
            updateEditedflag()
        elif updated_date[0] != editedMsgdate and editedMsgdate != (lastupdate[0]):
            updateMsgagain()
            print('Record has been updated again')
            print(updated_date[0])
            print(editedMsgdate)
            print(lastupdate[0])
        else:
            print('Record has been updated already')
    
    else:
        print('Record already exists or is not the type of record that gets added to the DB')


    if verbose == "true":
        #print(json_data)
        #print(time)
        #print(text)
        print(log_time)
        #print("This is the message that we are getting from the JSON DATA: "+str(message_id))
        #print("This is the last line that was written to the DB: "+str(lastid[0]))
        #print(userid)
        #print(new_id)
        #print (json.dumps(json_data,ensure_ascii=False,indent=2))

    #time.sleep(5)
    #break