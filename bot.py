import time
import datetime
import telepot
import psutil
import os
import socket
import pyowm
import googlemaps
import geocoder
from telepot.loop import MessageLoop
from subprocess import PIPE, Popen
from bs4 import BeautifulSoup
from lxml import html
from nsetools import Nse
import csv
import urllib2
import requests
import ConfigParams

import requests
import json
import re
import string
import random
import subprocess
import argparse
import threading
import cfscrape
import wikipedia
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global step
    file_id  =  ""
    chat_id = msg['chat']['id']
    command = ""
    user = ""
    step = 1
    if(content_type == "text"):
        chat_id = msg['chat']['id']
        command = msg['text']
        print("in text mode")
        user = msg['from']['first_name']
        print("Got command: %s" %command)

        if command == 'time':
            bot.sendMessage(chat_id, str(datetime.datetime.now()))

        #determining reply message based on the hourof day
        elif command == 'Hi' or command == 'hi' or command == 'HI' or command == 'hI':     #Hi Query
            replyMessage = "Hi "+ user + " "
            greeting = "It is sleeping time you still awake"
            hour = int(datetime.datetime.strftime(datetime.datetime.now(), '%H'))
            #print(hour)
            if(hour >= 4 and hour < 12):
                greeting = "Good Morning"
            elif(hour >= 12 and hour < 16):
                greeting = "Good Afternoon"
            elif(hour >= 16 and hour < 20):
                greeting = "Good Evening"

            replyMessage = replyMessage+greeting
            bot.sendMessage(chat_id, replyMessage)

        #gives various details of raspberry pi
        elif command.lower() == "How are you".lower():      #Health Query
            print("In Health Query")
            cpu_temparature = get_cpu_temparature()
            cpu_usage = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            ram_total = ram.total / 2**20       # MiB.
            ram_used = ram.used / 2**20
            ram_free = ram.free / 2**20
            ram_percent_used = ram.percent

            disk = psutil.disk_usage('/')
            disk_total = disk.total / 2**30     # GiB.
            disk_used = disk.used / 2**30
            disk_free = disk.free / 2**30
            disk_percent_used = disk.percent

            message = "I am doing as \nCPU Temparature "+str(cpu_temparature)+"C \nCPU Usage "+str(cpu_usage)+" \nRam Percent Used "+str(ram_percent_used)+" \nFree Disk Space "+ str(disk_free) + "Gb"
            bot.sendMessage(chat_id, message)

        #sends the local ip address and the wifi name to which it is connected to
        elif command.lower() == "Where are you".lower():
            print("telling where am I")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((ConfigParams.google_domain,80))
            ipaddr = s.getsockname()[0]
            wifi = Wireless('wlan0')
            wifiname = wifi.getEssid()

            message = "I am connected on "+ipaddr+" \nto WiFi "+wifiname
            bot.sendMessage(chat_id, message)
        elif command.lower()=="coming up cricket":
            print("fetching upcoming matches")

        elif command.lower().split("=")[0] == "mail" or command.lower().split("=")[0] == "Check mail" :
             email = command.split("=")[1]
             print(email)
             print ( '[+]'  + ' Bypassing Cloudflare Restriction...'  + '\n')
             bot.sendMessage(chat_id, '::This process takes time to gather all your data  One Moment Please.::')
             useragent = {'User-Agent' : 'pwnedornot'}
             cookies, user_agent = cfscrape.get_tokens('https://haveibeenpwned.com/api/v2/breachedaccount/test@example.com', user_agent='pwnedornot')
             time.sleep(2) 	# sleep 2 seconds to avoid rate limit
             addr = email   # r1 is the query for the account user enters
             r1 = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/{0}'.format(addr), headers= useragent, cookies= cookies, verify = True)
             check1 = r1.status_code #check1 is the status code for the account if we get a 404, account is not breached

             if check1 == 404:
             	print (  ' Account not pwned... :'  )
                bot.sendMessage(chat_id,'NO Results Found Your Email :'+ addr)
             	exit()
             else:
             	print ( '\n'  ' Account pwned...Listing Breaches...')
                json1 = r1.content.decode('utf8')
                simple1 = json.loads(json1)
                for item in simple1:
                    bot.sendMessage(chat_id,"".join(item['Title']+'\n'+item['BreachDate']))









        #if below command is cricket then it will fetch scrores from cricbuzz page
        elif command == "password" or command == "generate password " or command == "Pg" or command == "pg "  and step == 1:
            size = 8
            characters = string.digits+string.ascii_letters+string.punctuation+string.ascii_uppercase+string.ascii_lowercase
            p =  "".join(random.choice(characters) for x in range(size))
            print p
            password_message = 'your password is : ' + '\n'+ p +'\n' '\n created on : ' +str(datetime.datetime.now()) + '\n* save this message for future use *'
            bot.sendMessage(chat_id , password_message)



        elif command.lower().split("=")[0] == "wiki" :
            search = command.split("=")[1]
            wiki_search =  wikipedia.summary(search)
            print(wiki_search)
            bot.sendMessage(chat_id,wiki_search)


        elif command.lower().split("=")[0]=="scan":
            url_search = command.split("=")[1]
            bot.sendMessage(chat_id,'scanning url ')
            headers = {"Accept-Encoding": "gzip, deflate","User-Agent" : "gzip,  My Python requests library example client or username"}
            params = {'apikey': '81828642abc7ce5b5c4f52fc99a27f9f063a14c1b0de4127395d8385b12fead2', 'resource':url_search}
            r2 = requests.post('https://www.virustotal.com/vtapi/v2/url/report',params=params, headers=headers)
            json2 = r2.content.decode('utf8')
            simple2 = json.loads(json2)
            print(simple2)
            for json2 in simple2 :
                bot.sendMessage(chat_id,json2['scan_date'])










        elif command == "cricket" or command == "Cricket":

            resp = requests.get(ConfigParams.cric_url)
            soup = BeautifulSoup(resp.content, features="xml")
            items = soup.findAll('item' )
            cric_items = []
            for item in items:
                cric_item = {}
                cric_item['title'] = item.title.text
                cric_item['description'] = item.description.text
                cric_items.append(cric_item)
                print(cric_item)
                bot.sendMessage(chat_id,"".join(cric_item['title']+cric_item['description']))
        #used for downloading files uploaded to this bot
        elif command.lower().find("download") != -1:

            if command.split(".")[1] == "jpg" or command.split(".")[1] == "jpeg" or command.split(".")[1] == "png":
                try:
                    filename = '/root/Desktop/telegrambot/photos/'+command.split(" ")[1]
                    document = open(r'/root/Desktop/telegrambot/photos/'+command.split(" ")[1])
                except IOError:
                    bot.sendMessage(chat_id,"File not found")
            else:
                try:
                    filename = '/root/Desktop/telegrambot/documents/'+command.split(" ")[1]
                    document = open(r'/root/Desktop/telegrambot/documents/'+command.split(" ")[1])
                except IOError:
                    bot.sendMessage(chat_id,"File not found")

            bot.sendDocument(chat_id, document)


        elif command.lower().split(":")[0]=="news":
            resp = requests.get(ConfigParams.news_url)
            soup = BeautifulSoup(resp.content, features="xml")
            items = soup.findAll('item')
            news_items = []
            for item in items:
                news_item = {}
                news_item['title'] = item.title.text
                news_item['link'] = item.link.text
                news_items.append(news_item)
                print(items)
                bot.sendMessage(chat_id,"".join(news_item['title']+news_item['link']))
        else:
            message = "My Boss asked me to stay silent rather giving false information"
            bot.sendMessage(chat_id, message)


    #if user sent message is of photo or video or document then below code is used to store it on raspberry pi and download later
    elif(content_type == "document" or content_type == "photo" or content_type == "video"):
        if content_type == "document":
            file_id = msg['document']['file_id']
            file_name = msg['document']['file_name']

        elif content_type == "photo":
            file_id = msg['photo'][-1]['file_id']

        elif content_type == "video":
            file_id = msg['video']['file_id']

        bot.getUpdates()
        filereceived= bot.getFile(file_id)

        filepath = filereceived['file_path']

        file_name, file_extension = os.path.splitext(filepath)

        if content_type == "document":
            bot.download_file(file_id, "/root/Desktop/telegrambot/"+file_name+file_extension)
            bot.sendMessage(chat_id, "Received and stored your file "+file_name)
        elif content_type == "photo":
            bot.download_file(file_id, "/root/Desktop/telegrambot/"+file_name+file_extension)
            bot.sendMessage(chat_id, "Received and stored your photo "+file_name)
        elif content_type == "video":
            bot.download_file(file_id, "/root/Desktop/telegrambot/"+file_name+file_extension)
            bot.sendMessage(chat_id, "Received and stored your video "+file_name)

    #if user sent message is location then below code is executed
    elif content_type == 'location':
        location = msg['location']

        lat = location['latitude']
        lon = location['longitude']

        owm = pyowm.OWM(ConfigParams.open_weather_key)
        observation = owm.weather_at_coords(lat, lon)
        weather = observation.get_weather()
        location = observation.get_location()

        gmaps = googlemaps.Client(key=ConfigParams.google_key)
        geo_loc = str(lat), str(lon)
        g = geocoder.google(geo_loc,method='reverse')

        message = "***Weather&Location Statistics***"
        message = message+"\nCity : "+location.get_name()+"\nState : "+g.state+"\nPostalCode : "+g.postal+"\nTemp Max : "+str(weather.get_temperature('celsius')['temp_max'])+"\nTemp Min : "+str(weather.get_temperature('celsius')['temp_min'])+" \nStatus : "+weather.get_detailed_status()+"\nSunRise : "+weather.get_sunrise_time('iso')
        message = message+"\nSunSetTime : "+weather.get_sunset_time('iso')+"\n"

        bot.sendMessage(chat_id, message)




#to get cpu temparature of raspberry pi
def get_cpu_temparature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, error = process.communicate()
    return float(output[output.index('=') +1:output.rindex("'")])

#download the file which is present in uploaded from this bot application later
def download_file(download_url, dest):
    response = urllib2.urlopen(download_url)
    file = open(dest, 'w')
    file.write(response.read())
    file.close()
    print("Completed")



#read codes of stock companies registered in NSE based on company name
def readCodesFile(fileName, inputName):
    allcodes = {}
    with open(fileName) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            targets = row['companyname'].split(" ")
            var = 0
            while len(targets) > var :
                if inputName.lower() == (targets[var]).lower():
                    allcodes[row['companyname']] = row['code']
                    break;
                var = var + 1

    return allcodes

#algorithm to find the closest words even though spellings are wrong
def levenshteinDistance(s, t):
	if not s: return len(t)
	if not t: return len(s)
	if s[0] == t[0]: return levenshteinDistance(s[1:], t[1:])
	l1 = levenshteinDistance(s, t[1:])
	l2 = levenshteinDistance(s[1:], t)
	l3 = levenshteinDistance(s[1:], t[1:])
	return 1 + min(l1, l2, l3)


bot = telepot.Bot(ConfigParams.telegram_key)
bot.message_loop(handle)
print("I am listening ...")

while 1:
    time.sleep(10)
