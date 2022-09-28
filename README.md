# Introduction
This repository demonstrates how webscrapping can be used to monitor account activities on Ethereum blockchain. The target accounts are added in wallets.txt and the scripts will take accounts from that file. These accounts will be monitored for big transactions on their account. It can also be used to track ERO20 token movements of targetted accounts. Every time a movement is found, it will notify to you by sending message on your Telegram account.   

Onchain data is taken from Etherscan. Since we need many requests on Etherscan.com, the free API is not sufficient for this. In this repository shows how proxies and cookie data can be used to make repeated requests on Etherscan.

# How to use
1. **Fill config.config for Telegram API**. The messages will be forwarded to this Telegram account.      
2. Generate fake cookies to avoid getting Captcha   
    - Create x number of Etherscan accounts and login to them to get cookies. Store the login details and Cookies in *etherscan_cookies.py* file. In the file two examples shows how you need to add cookies. To get the proper values, do this in Firefox.   
    - Each time you login, one SID will be created. You can find SID in header. Store those SID separately in file *etherscan_sids.py*   
    - The file *firefoxdata.py* uses these data to generate headers and cookies for requests.   
3. Set up Proxies      
    - So many frequent requests from many different accounts can't be sent from same IP address. To fix that, we need Proxies.   
    - Purchase proxies from any trusted source and add its credentials to *proxysettings.ini*    
    - Add the Raw IP addresses to *user_proxies.py* file   
    - File *user_proxies.py* will generate the proxies for request and *proxy_supplier.py* will return proxy settings in random order
4. Fill *wallets.txt*
    - This file contains wallet address that you want to monitor. 
    - Write new address in new line
    - You can add any number of addresses here followed by their username (or the name you want to give them)    
5. Put your etherscan key in *settings.ini* file   
6. Change your log file from *settings.ini* file. The file *logger.py* handles logs.   

The headers and proxies are important to make huge number of requests on many accounts. They will be used in *monitor.py* to generate requests. The forwarding of messages on Telegram is handled by *telegram_messenger.py* file. If you can afford to purchase many proxies then you can avoid using fake cookies. 

