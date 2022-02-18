import socket
import select

listUsers = {}
sockets_list = []

class User:


    def __init__(self, name, connection):
        self.name = name 
        self.channel = "general"
        self.connection = connection

def addUser(name, connection):
	global listUsers
	listUsers[connection] = User(name, connection)
	return listUsers[connection]

def updateUser(user):
	global listUsers
	listUsers[user.connection] = user


def removeBySocket(client = None):
	global listUsers
	if (client):
		sendInBroadcast(" salio de la sala***", listUsers[client], True)
		del listUsers[client] #and class linked


def checkUsersBy(**kwargs):
	global listUsers
	if ("connection" in kwargs):
		if kwargs["connection"] in listUsers:
			return listUsers[kwargs["connection"]]
	elif ("name" in kwargs):
		for socket, user in listUsers.items():
			if 'name' in kwargs:
				if user.name == kwargs['name']:
					return True
	return False

def joinRoom(channel = None, selected_user = None):
	if ((selected_user != None) and (channel != None)):
		global listUsers
		for key, user in listUsers.items():
			if (user.channel == channel):
				sendInBroadcast(" salio de la sala***", selected_user, True)
				selected_user.channel = channel #set new channel to the user
				updateUser(selected_user)
				sendInBroadcast(" se ha unido a la sala***", selected_user, True)
				return True
		return False

def sendInBroadcast(message = None, sender = None, alertMsg = False):
	if ((message != None) and (sender != None)):
		global listUsers
		for key, user in listUsers.items():
			if (user.channel == sender.channel):
				msg = ""
				if (alertMsg):
					msg = "***"+sender.name+" "+message
				else:
					msg = "@"+sender.name+": "+message
				user.connection.sendall(msg.encode())


def getUsersByChannel(channel = None):
	if (channel != None):
		global listUsers
		names = ""
		for key, user in listUsers.items():
			if (user.channel == channel):
				names += user.name + " "
		return names


def routingCommand(typeMessage = None, connection = None):

	typeMsg = typeMessage.partition(" ")

	user = checkUsersBy(connection=connection)

	if not user:
		if (checkUsersBy(name=typeMsg[0])):
			message = str.encode("Nombre ya usado! Seleccione otro:")
			connection.sendall(message)
		else:
			userCreated = addUser(typeMsg[0], connection)
			message = str.encode("Bienvenido, "+typeMsg[0]+"!")
			connection.sendall(message)
			sendInBroadcast(" se ha unido a la sala***", userCreated, True)
	else:
		if typeMsg[0] == "/join":
			if (not joinRoom(typeMsg[2], user)):
				user.channel = typeMsg[2]
				updateUser(user)
			message = "Bienvenido a la sala "+user.channel
			user.connection.sendall(message.encode())
		elif typeMsg[0] == '/chat':
			if user.channel == "general":
				message = "Nos encontramos dentro de ninguna sala actualmente."
			else:
				message = "Actualmente estas en la sala "+user.channel
			user.connection.sendall(message.encode())
		elif typeMsg[0] == '/exit':
			if user.channel != "general":
				sendInBroadcast(" salio de la sala***", user, True)
				user.channel = "general"
				updateUser(user)
				sendInBroadcast(" se ha unido a la sala***", user, True)
				message = "Has vuelto a la sala GENERAL"
				user.connection.sendall(message.encode())
			else:
				message = "---"
				user.connection.sendall(message.encode())
				global sockets_list
				removeBySocket(user.connection)
				try:
					sockets_list.remove(user.connection)
				except ValueError:
					print("error during removing user socket")
		elif typeMsg[0] == '/onlineusers':
			names = getUsersByChannel(user.channel)
			message = "$("+user.channel+"): "+names
			user.connection.sendall(message.encode())
		else:
			sendInBroadcast(typeMessage, user)


def starting():
	HOST = '192.168.1.5'  # Standard loopback interface address (localhost)
	PORT = 64446        # Port to listen on (non-privileged ports are > 1023)
	

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind((HOST, PORT))
		server.listen()
		sockets_list = [server]
		print("Servidor inicializado")

		while True:

			read_sockets, _, _ = select.select(sockets_list, [], [])

			for notified_socket in read_sockets:

				if notified_socket == server:
					conn, addr = server.accept()
					data = conn.recv(1024)
					print("New user connected")
					typeMessage = data.decode('utf-8')
					routingCommand(typeMessage, conn)
					sockets_list.append(conn)
				else:
					data = notified_socket.recv(1024)

					if (len(data) == 0):
						print("User disconnected")
						sockets_list.remove(notified_socket)
						removeBySocket(notified_socket)
						continue

					typeMessage = data.decode('utf-8')
					routingCommand(typeMessage, notified_socket)