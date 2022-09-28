import time
def log(filename, message):
	with open(filename, 'a') as f:
		f.write('['+ time.strftime("%d-%m-%Y %I:%M:%S %p") +'] '+ message)