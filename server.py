from socket import *
import json

# "Database"
database = dict()

def startServer(serverPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Server has started!")

    try:
        while True:
            connectionSocket, addr = serverSocket.accept()

            setning = connectionSocket.recv(1024).decode()
            storeBokstaver = setning.upper()
            connectionSocket.send(storeBokstaver.encode())
            connectionSocket.close()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        closeServer(serverSocket)

def closeServer(serverSocket):
    serverSocket.close()
    print("Server socket closed.")

startServer(3000)