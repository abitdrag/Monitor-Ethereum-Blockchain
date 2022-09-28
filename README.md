# Introduction
This repository demonstrates how webscrapping can be used to monitor account activities on Ethereum blockchain. The target accounts are added in wallets.txt and the scripts will take accounts from that file. These accounts will be monitored for big transactions on their account. It can also be used to track ERO20 token movements of targetted accounts. 

Onchain data is taken from Etherscan. Since we need many requests on Etherscan.com, the free API is not sufficient for this. In this repository shows how proxies and cookie data can be used to make repeated requests on Etherscan.

# How to use
