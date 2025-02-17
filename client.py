from socket import *
import json

def startClient(serverName, serverPort):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    try:
        while True:
            setning = pick_input()
            if setning.lower() == "exit":
                clientSocket.send("exit".encode())
                break
            clientSocket.send(setning.encode())
            modifisertSetning = clientSocket.recv(1024)
            print(f"From server: {modifisertSetning.decode()}")
    finally:
        clientSocket.close()
        print("Connection closed.")

def send_request(request):
    pass

def pick_input():
    prompt = """
1. Legg til problem.
2. Vis alle eksisterende problemer.
3. Vis problem: (problem_ID).
4. Vis alternativ: (problem_ID).
5. Stem på alternativ: (problem_ID).
6. Vis stemmer: (problem_ID).
7. Skriv 'exit' for å avslutte.
"""
    print(prompt)
    choice = input("Velg handling: ")
    if choice == "1":
        return choice
    elif choice == "2":
        return choice
    elif choice == "3": 
        problem_ID = input("problem_ID: ")
        return choice
    elif choice == "4":
        problem_ID = input("problem_ID: ")
        return choice
    elif choice == "5":
        problem_ID = input("problem_ID: ")
        return choice
    elif choice == "6":
        problem_ID = input("problem_ID: ")
        return choice
    elif choice.lower() == "exit":
        return "exit"
    else:
        print("Invalid input, try again")
        pick_input()

def client():
    pass

startClient("localhost", 3000)
