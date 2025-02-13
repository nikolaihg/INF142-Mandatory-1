from socket import *
import json

def startClient(serverName, serverPort):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    setning = input("Input lowercase sentence: ")
    clientSocket.send(setning.encode())

    modifisertSetning = clientSocket.recv(1024)

    print(f"From server: {modifisertSetning.decode()}")
    clientSocket.close()

startClient("localhost", 3000)