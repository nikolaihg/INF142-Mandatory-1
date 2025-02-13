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

def send_request(request):
    pass

def pick_input():
    choice = input() #print options
    if choice == "":
        return ""
    elif choice == "":
        return ""
    elif choice == "": 
        return ""
    else:
        print("Invalid input, try again")
        pick_input()

def client():
    pass

startClient("localhost", 3000)