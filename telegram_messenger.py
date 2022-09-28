import requests
import re
import configparser
import sys
import os
import time
import logger

configParser = configparser.RawConfigParser()
configFilePath = r'config.config'
configParser.read(configFilePath)

key = configParser.get('telegram-settings', 'KEY')
channel_id = configParser.get('telegram-settings', 'CHANNEL')

configParser = configparser.RawConfigParser()
configFilePath = r'settings.ini'
configParser.read(configFilePath)

logfile = configParser.get('options', 'logfile')

def sendGet(url):
	try:
		response = requests.get(url, headers={'content-type':'application/json'})
		return response
	except Exception as e:
		logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Telegram ERROR: ' + str(e))

def decodeResponse(response):
	try:
		response = response.json()
		# print (response)
		mid = response['result']['message_id']
		return mid
	except Exception as e:
		logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Telegram ERROR: ' + str(e))

def sendMessage(message):
	# message has format text, images, tid, parent_tid
	baseurl = 'https://api.telegram.org/bot' + key
	url = baseurl + '/sendMessage?chat_id=' + channel_id + '&text=' + message[0]
	response = sendGet(url)
	return decodeResponse(response)