import socket
import threading
from utils import *

HOST = "127.0.0.1"
PORT = 8000
NAME = "Alice"
CHUNKSIZE = 1024

if __name__ == "__main__":
    # writing thread start
    tw = threading.Thread(target=writingMessage, args=(HOST,))
    tw.start()

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    print(f"{NAME}'s server port is {PORT}")
    
    # server listening
    serverSocket.listen(5)
    print("Server listening...")

    # connection with client
    # conn: socket object
    # addr: client ip
    conn, addr = serverSocket.accept()
    print(f"Bob {addr[0]}:{addr[1]} connected.")

    while True:
        clientMsg = conn.recv(CHUNKSIZE).decode()
        print("Bob says", clientMsg)

        if clientMsg.startswith("transfer") and len(clientMsg.split(' ')) == 2:
            filename = clientMsg.split(' ')[1]
            saveFilename = "new" + filename[0].upper() + filename[1:]

            readSaveFile(conn, saveFilename)

        # elif clientMsg == "quit":
        #     break

