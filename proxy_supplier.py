import user_proxies
import random

total_proxies = len(user_proxies.proxies_list)
index = random.randrange(total_proxies)

def get_proxy():
	global index, total_proxies
	proxy = user_proxies.proxies_list[index]
	index = (index + 1) % total_proxies
	return proxy