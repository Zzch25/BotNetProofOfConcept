#Zachary Job
#25/25/25
#
#server_netload.py
#
#Innocent botnet server payload function proof of concept
#
#This is a basic serial operation so it can be easily demoed

import pickle
import Queue

def serverEndProc(dataQueue):

	resultList = dataQueue.get()
	resultList = resultList + dataQueue.get()

	return resultList
