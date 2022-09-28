import requests
import time
import configparser
import sys
import firefoxdata
import proxy_supplier
import logger
import web3
from ethtoken.abi import EIP20_ABI # this ABI works for ERC20 tokens
from bs4 import BeautifulSoup
import re
import telegram_messenger as tg
import random

configParser = configparser.RawConfigParser()
configFilePath = r'settings.ini'
configParser.read(configFilePath)

etherscankey = configParser.get('options', 'etherscankey')
logfile = configParser.get('options', 'logfile')

def get_wallets(filename):
	wallets = []
	usernames = {}
	with open(filename, 'r') as f:
		lines = f.readlines()
	for line in lines:
		tline = line.split(' ', 1)
		w = tline[0].lower().strip()
		wallets.append(w)
		try:
			usernames[w] = tline[1].strip()
		except:
			usernames[w] = 'Anon'
	return (wallets, usernames)

def get_data_from_soup(soup):
	all_divs = soup.find_all('div', attrs = {'class':'row'}) # all divs with class row
	transaction_action = ''
	eth_value = ''
	eth_price = ''
	for div in all_divs:
		# look for transaction action
		if 'Transaction Action:' in div.text:
			sub_divs = div.find_all("div", attrs = {'class':'media-body'})
			if len(sub_divs) > 0:
				# checking only last action
				sub_div = sub_divs[len(sub_divs)-1]
				for element in sub_div.contents:
					temp = element.text
					if len(temp) > 0:
						if temp.replace('.','',1).isdigit():
							temp = round(float(temp), 2)
						transaction_action = transaction_action + ' ' + str(temp)
		# # look for ETH value
		# if 'Value:' in div.text:
		# 	value_result = div.find_all(id="ContentPlaceHolder1_spanValue")
		# 	if len(value_result) > 0:
		# 		eth_value = value_result[0].text
		# 	else:
		# 		eth_value = 'Not found'
		# # look for ETH price
		# if 'Ether Price:' in div.text:
		# 	price_result = div.find_all(id="ContentPlaceHolder1_spanClosingPrice")
		# 	if len(price_result) > 0:
		# 		eth_price = price_result[0].text
		# 	else:
		# 		eth_price = 'Not found'
	# log any errors
	if transaction_action == '':
		logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] CRITICAL ERROR: Transaction Action not found')
	# if eth_value == 'Not found' and eth_price == 'Not found':
	# 	logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] CRITICAL ERROR: Value and Price not found')
	return transaction_action.strip()

def create_message(tx_hash, wallet, username, contract_addr):
	emoticons = ['✈️','🚀','🚘','🤑']
	while True:
		proxy = proxy_supplier.get_proxy() # http://username:password@ip_address:port
		# create proxies
		proxies = {
			"http": proxy,
			"https": proxy,
		}
		headers = firefoxdata.get_headers(wallet)
		cookies, sid = firefoxdata.get_cookies() # sid is not required in this case
		url = 'https://etherscan.io/tx/'+tx_hash
		try:
			r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=3)
			if r.status_code != 200:
				logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] ERROR: (couldn\'t fetch etherscan page, retry in 1 sec.. )' + str(int(r.status_code)))
				time.sleep(1)
			else: break
		except Exception as e:
			logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] ERROR: '+ str(e))
	tsoup = BeautifulSoup(r.text, 'html.parser')
	transaction_action = get_data_from_soup(tsoup)
	# # create result to return
	# try:
	# 	if eth_price == 'Not found' and eth_value != 'Not found': # buy action
	# 		usd_value = float(re.search(r'\(\$.+\)', eth_value).group(0)[2:-1]) # usd value in float
	# 		token_amount = float(transaction_action.split(' ')[4])
	# 		token_price = usd_value/token_amount
	# 	else: # sell action
	# 		token_price = float(transaction_action.split(' ')[4]) * float(eth_price[1:].split('/')[0].strip())
	em = random.choice(emoticons)
	etherscanlink = 'https://etherscan.io/tx/'+tx_hash
	uniswaplink = 'https://uniswap.info/token/' + contract_addr
	message = em + ' ' + transaction_action + ' ' + em + '\n\n' + \
		uniswaplink + '\n\n' + \
		etherscanlink + '\n\n' + \
		wallet + ' (' + username + ')'
	
	return (True, message)
	# return (True, wallet + ' (**'+ username +'**)\n' + transaction_action + '\nTx: https://etherscan.io/tx/' + tx_hash + '\nDextools: https://www.dextools.io/app/uniswap/pair-explorer\nUniswap: https://app.uniswap.org/#/swap?inputCurrency='+ contract_addr +'&outputCurrency=ETH')


def send_to_tg(message):
	mid = tg.sendMessage(message)
	return mid

if __name__ == '__main__':
	walletfile = 'wallets.txt'
	starttime = int(time.time())
	seen_txns = {}
	w = web3.Web3(web3.HTTPProvider('https://api.myetherwallet.com/eth'))
	while True:
		wallets, usernames = get_wallets(walletfile)
		for wallet in wallets:
			erc20_txn_url = 'https://api.etherscan.io/api?module=account&action=tokentx&address='+wallet+'&page=1&offset=5&sort=desc&apikey='+etherscankey
			try:
				r = requests.get(erc20_txn_url)
				result = r.json()['result']
			except Exception as e:
				logger.log(logfile, 'ERROR! Fetching ERC20 txs for ' + wallet + ': ' + str(e))
				result = []
			if wallet not in seen_txns:
				seen_txns[wallet] = []
			for item in reversed(result):
				tx_hash = item['hash']
				time_stamp = item['timeStamp']
				if time_stamp < starttime: # old transaction, add to seen_txns
					seen_txns.append(tx_hash)
					continue # skip current and continue with next
				from_addr = item['from']
				to_addr = item['to']
				contract_addr = item['contractAddress']
				token_name = item['tokenName']
				
				if 'uniswap' in token_name.lower():
					continue # skip current but don't add to seen_txns
				if tx_hash not in seen_txns[wallet]: # these are new transactions
					try:
						contract = w.eth.contract(w.toChecksumAddress(from_addr), abi=EIP20_ABI)
						from_name = contract.functions.name().call()
					except:
						from_name = 'No name'
					try:
						contract = w.eth.contract(w.toChecksumAddress(to_addr), abi=EIP20_ABI)
						to_name = contract.functions.name().call()
					except:
						to_name = 'No name'

					if 'uniswap' in from_name.lower() or 'uniswap' in to_name.lower(): # make sure it is uniswap txn
						# we have got an unseen uniswap transaction
						# create message from tx details
						status, message = create_message(tx_hash, wallet, usernames[wallet], contract_addr) # returns a tuple (True/False, message)
						if status == True:
							mid = send_to_tg(message)
							logger.log(logfile, '['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] INFO: message sent ID = ' + str(mid))
					# append transaction hash to seen list
					seen_txns[wallet].append(tx_hash)
			time.sleep(0.2)