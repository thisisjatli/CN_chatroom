import socket
import os

CHUNKSIZE = 1024

def transferFile(clientSocket, filename):
    print("Start transfering...")
    with open(filename, 'rb') as fr:
        filesize = os.stat(filename).st_size
        clientSocket.send(str(filesize).encode())
        data = fr.read(CHUNKSIZE)
        while data:
            clientSocket.send(data)
            data = fr.read(CHUNKSIZE)
        fr.close()
        
    print("Finish transfering.")
    return

def receiveFile(conn):
    filename = conn.recv(CHUNKSIZE).decode()
    filename = "new" + filename[0].upper() + filename[1:]
    print("Start uploading...")
    filesize = int(conn.recv(CHUNKSIZE).decode())

    with open(filename, 'wb') as fw:
        while filesize > 0:
            # receive data from client and save to local disk
            data = conn.recv(CHUNKSIZE)
            fw.write(data)
            filesize = filesize - CHUNKSIZE
        fw.close()

    print("Finish uploading.")
    return

def writingMessage(host):
    serverPort = int(input("Please type in a port number:"))

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, serverPort))

    # get greetings from server, respond with name
    serverMsg = clientSocket.recv(CHUNKSIZE).decode()
    name = input(serverMsg)
    clientSocket.send(name.encode())

    while True:
        msg = input("Enter your message:")
        if msg.startswith("transfer") and len(msg.split(' ')) == 2:
            filename = msg.split(' ')[1]
            clientSocket.send(msg.encode())
            transferFile(clientSocket, filename)
        # elif msg == "quit":
        #     break
        else:    
            clientSocket.send(msg.encode())

def readSaveFile(conn, filename):
    filesize = int(conn.recv(CHUNKSIZE).decode())
    print("Start transfering...")

    with open(filename, 'wb') as fw:
        while filesize > 0:
            # receive data from client and save to local disk
            data = conn.recv(CHUNKSIZE)
            fw.write(data)
            filesize = filesize - CHUNKSIZE
        fw.close()

    print("Finish transfering.")
    return