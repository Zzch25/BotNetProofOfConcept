#Zachary Job
#25/25/25
#
#server.py
#
#Innocent botnet proof of concept
#
#Unlike a final design which would load the client manifest and array of
#system and client functions, this is a hard coded example

import sys
import socket
import Queue
import types
import threading
import dill as pickle

from client_netload import listModify
from server_netload import serverEndProc

#The scenario occuring here is depicted in the README
#REMEMBER, this is a quarter baked, hard coded, proof of concept
#The final version of something like this would require an array
#of functions and manifest to manage a complex transaction

#--------------------------------------------------------------
#----------------------General Definitions---------------------
#--------------------------------------------------------------

#For tasking the client with one function and set of data
#
#@PARAMS: Self explanatory, no explanation will be provided
def setClient(server_sock, funcClient, dataClient, server_port, server_addr, client_port, client_addr, returnData):

	BUFF = 4096
	cond = True

	print 'Receiving connection... %s %d\n' % (client_addr, client_port)

	server_sock_accept, address = server_sock.accept()

	print 'Preparing connection...\n'

	client_sock = socket.socket();
	
	while cond:
		try:
			cond = False
			client_sock.connect((client_addr, client_port))
		except Exception as e:
			print "Failure to connect @ SERVER @ 0\n"
			cond = True

	#Client tasking
	print 'Sending...'
	lenSend = funcClient.read(1024)
	while(lenSend):
		print 'Sending...'
		client_sock.send(lenSend)
		lenSend = funcClient.read(1024)
	
	client_sock.close()
	
	print "Offloaded\nAwaiting Confirmation"

	server_sock_accept.recv(1)

	print "Confirmed\nSending Data"
	
	client_sock = socket.socket();

	cond = True

	while cond:
		try:
			cond = False
			client_sock.connect((client_addr, client_port))
		except Exception as e:
			print "Failure to connect @ SERVER @ 0\n"
			cond = True

	data = pickle.dumps(dataClient)
	client_sock.send(data)

	client_sock.close()

	print "Offloaded\nAwaiting Result Size"

	server_sock_accept, address = server_sock.accept()

	szResult = int(server_sock_accept.recv(BUFF), 16)

	server_sock_accept.close()

	print "Confirmed\nInitiating Receive"

	client_sock = socket.socket();

	cond = True

	while cond:
		try:
			cond = False
			client_sock.connect((client_addr, client_port))
		except Exception as e:
			print "Failure to connect @ SERVER @ 0\n"
			cond = True

	client_sock.send("1")

	print "Sent\nAwaiting data"

	server_sock_accept, address = server_sock.accept()

	returnData.put(pickle.loads(server_sock_accept.recv(szResult)));

	print "Completed"

	client_sock.close()
	server_sock_accept.close()


#For controlling server side functions
#
#@PARAMS: No need to explain the parameters, they are simple
def setServer(dataQueue, funcServer, dataServer):

	with open(funcServer, 'rb') as func:
		raw = pickle.load(func)

	serverProc = types.FunctionType(raw, globals())

	return serverProc(dataQueue)

#--------------------------------------------------------------
#----------------------------MAINS-----------------------------
#--------------------------------------------------------------

#Generic network initialization

server_port0 = int(sys.argv[1])
server_port1 = int(sys.argv[2])
server_addr = '127.0.0.1'

server_sock0 = socket.socket()
server_sock0.bind((server_addr, server_port0))
server_sock0.listen(5)

server_sock1 = socket.socket()
server_sock1.bind((server_addr, server_port1))
server_sock1.listen(5)

client_0_port = int(sys.argv[4])
client_0_addr = sys.argv[3]
client_1_port = int(sys.argv[6])
client_1_addr = sys.argv[5]

#Emulate pickling from tasker
with open('client_0.func', 'wb') as toArmC0:
	pickle.dump(listModify.__code__, toArmC0)
with open('client_1.func', 'wb') as toArmC1:
	pickle.dump(listModify.__code__, toArmC1)
with open('server.func', 'wb') as toArmS0:
	pickle.dump(serverEndProc.__code__, toArmS0)

#Emulate receiving functions and data
funcClient0 = open('client_0.func','rb')
funcClient1 = open('client_1.func','rb')
funcServer = 'server.func'

dataClient0 = [[1,1,2,3,4,8],1,[1,[client_1_port,client_1_addr]]]
dataClient1 = [[5,6,7,8,8,1],0,[1,[client_0_port,client_0_addr]]]
dataServer = [2,[client_0_port,client_0_addr],[client_1_port,client_1_addr]]

#Task the clients
returnData = Queue.Queue()
threading.Thread(target=setClient, args=(server_sock0, funcClient0, dataClient0, server_port0, server_addr, client_0_port, client_0_addr, returnData)).start()
threading.Thread(target=setClient, args=(server_sock1, funcClient1, dataClient1, server_port1, server_addr, client_1_port, client_1_addr, returnData)).start()

#After the clients have enqueued their results, feed to server
result = setServer(returnData, funcServer, dataServer)
print ""
print result

#Cleanup
funcClient0.close()
funcClient1.close()
server_sock0.close()
server_sock1.close()



