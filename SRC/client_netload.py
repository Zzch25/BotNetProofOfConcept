#Zachary Job
#25/25/25
#
#client_netload.py
#
#Innocent botnet payload function proof of concept
#
#This is a basic serial operation so it can be easily demoed

import socket
import operator

#A simple demo of basic functions
#Find the most frequent number in a list, share it with
#another client and receive it's most frequent, then zero
#the two frequent characters
#
#@PARAM: All needed data stored via list
#@PARAM: The rest are self explanatory
def listModify(data, server_port, server_addr):
	
	BUFF = 4096
	cond = True

	#Initialize and get the max occured value
	result = data[0]
	lst = data[0]
	maxOccur = max(set(lst), key=lst.count)
	print maxOccur

	print "Binding %s %d" % (server_addr, server_port)

	#Setup connections
	server_sock = socket.socket()
	server_sock.bind((server_addr, server_port))
	server_sock.listen(5)

	client_addr = data[2][1][1]
	client_port = data[2][1][0]
	client_sock = socket.socket();

	recvMaxOccur = 0

	print "Target address :: %s %d\n" % (client_addr, client_port)

	if data[1] == int(1):
		print "Attempting connect"

		while cond:
			try:
				cond = False
				client_sock.connect((client_addr, client_port))
			except Exception as e:
				print "Failure to connect @ CNL @ 0\n"
				cond = True
		
		print 'Awaiting Accept'

		server_sock_accept, address = server_sock.accept()
		
		print "Offloading"

		szResult = client_sock.send(str(maxOccur))

		print "Success\nAccepting data"

		recvMaxOccur = int(server_sock_accept.recv(BUFF));

		print "Recieved"

	else:	
		print 'Awaiting Accept'

		server_sock_accept, address = server_sock.accept()

		print "Attempting connect"

		while cond:
			try:
				cond = False
				client_sock.connect((client_addr, client_port))
			except Exception as e:
				print "Failure to connect @ CNL @ 1\n"
				cond = True

		print "Awaiting data"

		recvMaxOccur = int(server_sock_accept.recv(BUFF));

		print "Received\nOffloading"

		szResult = client_sock.send(str(maxOccur))

		print "Done"

	client_sock.close()
	server_sock.close()
	server_sock_accept.close()

	#Update the result as described
	i = 0
	for elems in result:
		if elems == maxOccur or elems == recvMaxOccur:
			result[i] = 0
		i += 1

	return result		
