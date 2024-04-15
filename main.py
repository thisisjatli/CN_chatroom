import socket
import threading
from utils import *

PORT = 8000
HOST = "127.0.0.1"

if __name__ == "__main__":
    # writing thread start
    tw = threading.Thread(target=writingMessage, args=(HOST,))
    tw.start()

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            serverSocket.bind((HOST, PORT))
            break
        except:
            PORT = PORT + 1

    print(f"Server port is {PORT}")
    
    # server listening
    serverSocket.listen(5)
    print("Server listening...")

    # connection with client
    # conn: socket object
    # addr: client ip
    conn, addr = serverSocket.accept()
    print(f"Client {addr[0]}:{addr[1]} connected.")

    # ask for client's name
    welcomeMsg = "Greetings from server, what's your name?"
    conn.send(welcomeMsg.encode())

    clientName = conn.recv(CHUNKSIZE).decode()
    print("Client's name is", clientName)

    while True:
        clientMsg = conn.recv(CHUNKSIZE).decode()
        print(f"{clientName} says", clientMsg)

        if clientMsg.startswith("transfer") and len(clientMsg.split(' ')) == 2:
            filename = clientMsg.split(' ')[1]
            saveFilename = "new" + filename[0].upper() + filename[1:]

            readSaveFile(conn, saveFilename)

        # elif clientMsg == "quit":
        #     break