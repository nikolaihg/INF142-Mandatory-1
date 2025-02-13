from socket import *
import json

# "database"
database = dict()

def show_votes(problem):
    pass

def show_problem(problem_ID):
    pass

def show_problems():
    pass

def start_server(serverPort):
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
        close_server(serverSocket)

def close_server(serverSocket):
    serverSocket.close()
    print("Server socket closed.")

start_server(3000)