from socket import *
import json

serverPort = 3000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("Til tjeneste!")

while True:
    connectionSocket, addr = serverSocket.accept()

    setning = connectionSocket.recv(1024).decode()
    storeBokstaver = setning.upper()
    connectionSocket.send(storeBokstaver. encode())
    connectionSocket.close()