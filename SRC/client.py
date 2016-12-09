#Zachary Job
#25/25/25
#
#client.py
#
#Innocent botnet proof of concept
#
#This is a naive model, it does not handle failover or any
#advanced conlficts. It too is partially hard coded

import sys
import socket
import types
import dill as pickle

#The scenario occuring here is depicted in the README
#REMEMBER, this is a quarter baked, hard coded, proof of concept
#The final version of something like this would require an array
#of functions and manifest to manage a complex transaction

#--------------------------------------------------------------
#----------------------General Definitions---------------------
#--------------------------------------------------------------

#Receive data necesary to run the client
#
#@PARAMS: Self explanatory, no explanation will be provided
def getData(server_sock, funcClient, client_addr, client_port):

	BUFF = 4096
	BUFF_FILE = 1024
	cond = True

	print 'Preparing connection...\n'

	client_sock = socket.socket();
	
	while cond:
		try:
			cond = False
			client_sock.connect((client_addr, client_port))
		except Exception as e:
			print "Failure to connect @ CLIENT @ 0\n"
			cond = True
	
	print 'Preparing receiver'

	server_sock_accept, address = server_sock.accept()
	
	func = open(funcClient,'wb')

	print "Receiving"

	lenRead = server_sock_accept.recv(BUFF_FILE)
	while (lenRead):
		print "Receiving"
		func.write(lenRead)
		lenRead = server_sock_accept.recv(BUFF_FILE)

	server_sock_accept.close()

	print "Done Receiving\nInforming Server"

	client_sock.send("1")

	print "Receiving"

	server_sock_accept, address = server_sock.accept()

	inData = []
	iterData = (server_sock_accept.recv(BUFF_FILE))
	inData.append(iterData)

	while (iterData):
		print "Receiving"
		iterData = server_sock_accept.recv(BUFF_FILE)
		if (iterData):
			inData.append(iterData)

	lenData = pickle.loads(''.join(inData))

	print "Done"

	func.close()
	client_sock.close()
	server_sock_accept.close()
	
	return lenData

#Produce results as programmed in the function
#
#@PARAMS: Self explanatory, no explanation will be provided
def runFunc(client_data, funcClient, client_port, client_addr):

	with open(funcClient, 'rb') as func:
		raw = pickle.load(func)

	clientProc = types.FunctionType(raw, globals())

	return clientProc(client_data, client_port, client_addr)

#Offload the result to the server
#
#@PARAMS: Self explanatory, no explanation will be provided
def offloadResult(server_sock, result, client_addr, client_port):
	
	cond = True
	
	print 'Preparing connection...\n'

	client_sock = socket.socket();
	
	while cond:
		try:
			cond = False
			client_sock.connect((client_addr, client_port))
		except Exception as e:
			print "Failure to connect @ CLIENT @ 1\n"
			cond = True

	print "Sending Result Size"

	client_sock.send(hex(sys.getsizeof(result)))

	client_sock.close()

	print 'Preparing receiver'

	server_sock_accept, address = server_sock.accept()

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
			print "Failure to connect @ CLIENT @ 1\n"
			cond = True

	data = pickle.dumps(result)
	client_sock.send(data)

	client_sock.close()
	server_sock_accept.close()

#--------------------------------------------------------------
#----------------------------MAINS-----------------------------
#--------------------------------------------------------------

FUNC_FILE = 'client_func'

server_port = int(sys.argv[3])
server_addr = sys.argv[2]

client_port = int(sys.argv[1])
client_addr = '127.0.0.1'

print "Preparing for server connection from... %s %d" % (client_addr, client_port)

client_sock = socket.socket()
client_sock.bind((client_addr, client_port))
client_sock.listen(5)

clientData = getData(client_sock, FUNC_FILE, server_addr, server_port)

client_sock.close()

result = runFunc(clientData, FUNC_FILE, client_port, client_addr)

print "Preparing for server connection"

client_sock = socket.socket()
client_sock.bind((client_addr, client_port))
client_sock.listen(5)

offloadResult(client_sock, result, server_addr, server_port)

client_sock.close()

