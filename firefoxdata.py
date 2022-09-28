import etherscan_cookies
import etherscan_sids

cookies_list = etherscan_cookies.cookies_list
sid_list = etherscan_sids.sid_list

total_cookies = len(cookies_list)
next_index = 0

def get_headers(addr):
	my_referer = 'https://etherscan.io/address-tokenpage?m=normal&a=' + addr.lower()
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
				'Accept-Encoding': 'gzip, deflate',
				'Accept': '*/*',
				'Connection': 'keep-alive',
				'Referer': my_referer,
				'set-fetch-dest': 'document',
				'set-fetch-mode': 'navigate',
				'set-fetch-site': 'none',
				'upgrade-insecure-requests': '1'}
	return headers

def get_cookies():
	global cookies_list, next_index, sid_list
	# random_index = randrange(total_cookies)
	t = cookies_list[next_index]
	s = sid_list[next_index]	
	next_index = (next_index + 1)%total_cookies
	return (t, s)