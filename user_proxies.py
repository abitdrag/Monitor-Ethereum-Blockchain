import configparser
import logger

configParser = configparser.RawConfigParser()
configFilePath = r'proxysettings.ini'
configParser.read(configFilePath)

username = configParser.get('proxy', 'proxy_username')
password = configParser.get('proxy', 'proxy_password')

configParser = configparser.RawConfigParser()
configFilePath = r'settings.ini'
configParser.read(configFilePath)

logfile = configParser.get('options', 'logfile')

# add your IP addresses here
raw_list = [
	# '127.0.0.1:5000',
]

proxies_list = []
for entry in raw_list:
	proxies_list.append('http://' + username + ':' + password + '@' + entry)

# print(str(len(proxies_list)) + ' proxies imported!!')
logger.log(logfile, str(len(proxies_list)) + ' proxies imported!!')