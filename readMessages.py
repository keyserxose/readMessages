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
myid = int(config['USERS']['myid'])
alexid = int(config['USERS']['alexid'])
faid = int(config['USERS']['faid'])

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


#GET JSON DATA from Telegram API - DEV
receive_data="https://api.telegram.org/bot"+str(apiKey_dev)+"/GetUpdates?offset=-1&limit=1"



# Send function
#def send():
#    requests.post(bot_chat+message)



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
    cursor.execute('INSERT INTO messages(messageid, message, user, first_name, chatname, date) VALUES(?, ?, ?, ?, ?, datetime())',(message_id, text, username, first_name, chatName, ))
    db.commit()

#Seach for a message to edit
#def getupdatedMsg():
#    cursor.execute('SELECT messageid FROM messages WHERE messageid = ?', (editedMsgId,))

#Update the message
def updateMsg():
    cursor.execute('UPDATE messages set message = ?, edited = ?, updated_date = ? where messageid = ?', (editedMsg, edited, editedMsgdate, editedMsgId,))
    db.commit()

## Add function here to check the edit_date in the DB so we don't edit the record every time
def checkIfupdated():
    cursor.execute('SELECT updated_date FROM messages WHERE messageid = ?', (editedMsgId,))
    global updated_date
    updated_date = cursor.fetchone()



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

    message_id = None
    editedMsgId = None
    editedMsg = None
    #editedMsgdate = None

    #text = None
    message_id = None
    userid = None
    username = None
    first_name = None
    chatid = None
    chatName = None

    #text = None
    #photo = None

    #test = json_data['result'][0]['edited_message']
    #print(test)

    #break

    #time.sleep(5)

    #try:
    #    if 'message' in json_data['result'][0]:
    #        print('This is an normal message')
    #    elif 'photo' in json_data['result'][0]['message']:
    #        print('This is a photo')
    #    elif 'edited_message' in json_data['result'][0]:
    #        print('This is an edited message')
    #    else:
    #        print('This is other type of message')
    #except:
    #    print('Nothin')
    #    pass
    #
    #break
    # This deals with normal messages in group chats
    if 'message' in json_data['result'][0] and  json_data['result'][0]['message']['chat']['type'] == 'group':
        print('This is an anything in a group')
        if 'text' in json_data['result'][0]['message']:
            print('This is a message')
            text = json_data['result'][0]['message']['text'] # This gets the message
            message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
            userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
            username = json_data['result'][0]['message']['from']['username'] # This gets the username
            first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
            chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
            chatName = json_data['result'][0]['message']['chat']['title'] # This gets the chat Name
        else:
            print('Whatever this is, I dont care for it')

    # This deals with edited messages in group chats
    elif 'edited_message' in json_data['result'][0] and json_data['result'][0]['edited_message']['chat']['type'] == 'group':
        print('This anythin edited message in a group')
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
        #elif 'photo' in json_data['result'][0]['message']:
        #    print('This is a photo')
        #elif 'animation' in json_data['result'][0]['message']:
        #    print('this is a GIF')
        #elif 'poll' in json_data['result'][0]['message']:
        #    print('This is a poll')

    # This deals with edited messages in private chats
    elif 'edited_message' in json_data['result'][0] and json_data['result'][0]['edited_message']['chat']['type'] == 'private':
        print('This anything edited in a private chat')
        if 'text' in json_data['result'][0]['edited_message']:
            print('This is an edited message')
            editedMsg = json_data['result'][0]['edited_message']['text'] # This gets the edited message text 
            editedMsgId = json_data['result'][0]['edited_message']['message_id'] # This gets the edited message ID
            editedMsgdate = json_data['result'][0]['edited_message']['edit_date'] # This gets the edited message date
            date = json_data['result'][0]['edited_message']['date'] # This gets the original message date
        else:
            print('Whatever this is, I dont care for it')
        #elif 'photo' in json_data['result'][0]['edited_message']:
        #    print('This is a photo')
        #elif 'animation' in json_data['result'][0]['edited_message']:
        #    print('this is a GIF')
        
        #try:
        #    text = json_data['result'][0]['message']['text'] # This gets the message
        #    message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
        #    userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
        #    username = json_data['result'][0]['message']['from']['username'] # This gets the username
        #    first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
        #    chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
        #except KeyError:
        #    photo = json_data['result'][0]['message']['photo'] # This gets the message
        #    print("DB doesn't allow to save photos, an Exception has occurred, we will keep going")
        #    pass
        #except KeyError:
        #    animation = json_data['result'][0]['message']['animation']
        #    print("DB doesn't allow to save GIFs, an Exception has occurred, we will keep going")
        #    pass
    
    else:
        print('This is other type of message')

    
    #time.sleep(3)
    #break

    #Geeting the type of chat (group or private)
    #try:
    #    chatType = json_data[0][1]['message']['chat']['type']
    #except KeyError:
    #    chatType = json_data[5]

#READING JSON
    #if chatType == 'group':
    #    try:
    #        text = json_data['result'][0]['message']['text'] # This gets the message
    #        message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
    #        userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
    #        username = json_data['result'][0]['message']['from']['username'] # This gets the username
    #        first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
    #        chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
    #        chatName = json_data['result'][0]['message']['chat']['title'] # This gets the chat Name
    #    except KeyError:
    #        editedMsg = json_data['result'][0]['edited_message']['text'] # This gets the edited message text 
    #        editedMsgId = json_data['result'][0]['edited_message']['message_id'] # This gets the edited message ID
    #        editedMsgdate = json_data['result'][0]['edited_message']['edit_date'] # This gets the edited message date
    #        date = json_data['result'][0]['edited_message']['date'] # This gets the original message date
    #        pass
    
#Reading JSON Data
    #try:
    #    text = json_data['result'][0]['message']['text'] # This gets the message
    #    message_id = json_data['result'][0]['message']['message_id'] # This gets the message_id to avoid re-sending data
    #    userid = json_data['result'][0]['message']['from']['id'] # This gets the user_id
    #    username = json_data['result'][0]['message']['from']['username'] # This gets the username
    #    first_name = json_data['result'][0]['message']['from']['first_name'] # This gets the first_name
    #    chatid = json_data['result'][0]['message']['chat']['id'] # This gets the chat_id
    #    chatName = json_data['result'][0]['message']['chat']['title'] # This gets the chat Name
    #except KeyError: #This deals with the exceptions
    #    editedMsg = json_data['result'][0]['edited_message']['text'] # This gets the edited message text 
    #    editedMsgId = json_data['result'][0]['edited_message']['message_id'] # This gets the edited message ID
    #    editedMsgdate = json_data['result'][0]['edited_message']['edit_date'] # This gets the edited message date
    #    date = json_data['result'][0]['edited_message']['date'] # This gets the original message date
    #    print(datetime.now())
    #    print("An Exception has ocurred, we will keep going")
    #    pass
    #except NameError:
    #    pass

    #Read DB File
    #readDbFile()

    # Read from SQLITE DB
    getId()

    # Check Edited message date
    checkIfupdated()

    #print('This is the message id in case this is a new message: '+str(message_id))

    #print('This is the Edited Message ID: '+str(editedMsgId))

    #print('This is the new text for the edited message: '+str(editedMsg))

    #print('This is the last id in the DB: '+str(lastid[0]))

    #print(editedMsgdate)

    #print(updated_date[0])

    #print(editedMsgId)
    #Checking if message has been sent
    #if int((lastid)[0]) == message_id:
    #    print("Checking SQLITE DB, Message has already been sent")
        #time.sleep(2)
    #Sending Messages 
        
    #Successful messages

    #Write DB File
    #writeDbFile()

    # Write to SQlite DB and close connection
    if message_id != None and message_id != int((lastid)[0]):
        writeId()
        print('Adding record to DB')
    elif editedMsgId != None and editedMsgId == int((lastid)[0]) and editedMsgdate != (updated_date[0]):
        edited = 1
        updateMsg()
        print('Updating Message')
        #print(editedMsg)
        #print(editedMsgdate)
        #print(updated_date)
    
    else:
        print('Record already exists or is not the type of record that gets added to the DB')

    #time.sleep(3)

    #db.close()

    #if editedMsgId == int((lastid)[0]):
    #    updateMsg()
    #    print('Updating Message')



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

    time.sleep(5)
    #break