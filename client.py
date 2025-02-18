from socket import *
import json

PROMPT = """
1. (POST problem) Legg til problem.
2. Vis alle eksisterende problemer.
3. Vis problem: (problem_ID).
4. Vis alternativ: (problem_ID).
5. Stem på alternativ: (problem_ID).
6. Vis stemmer: (problem_ID).
7. Skriv 'exit' for å avslutte.
"""

def startClient(serverName, serverPort, prompt):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    try:
        while True:
            choice = pick_input(prompt)
            if choice.lower() == "exit":
                clientSocket.send("exit".encode())
                break
            clientSocket.send(choice.encode())
            modifisertSetning = clientSocket.recv(1024)
            print(f"From server: {modifisertSetning.decode()}")
    finally:
        clientSocket.close()
        print("Connection closed.")

def pick_input(prompt):
    print(prompt)
    choice = input("Velg handling: ")
    if choice == "1":
        return choice
    elif choice == "2":
        return choice
    elif choice == "3": 
        problem_ID = input("problem_ID: ")
        return choice + " " + problem_ID
    elif choice == "4":
        problem_ID = input("problem_ID: ")
        return choice + " " + problem_ID
    elif choice == "5":
        problem_ID = input("problem_ID: ")
        return choice + " " + problem_ID
    elif choice == "6":
        problem_ID = input("problem_ID: ")
        return choice + " " + problem_ID
    elif choice.lower() == "exit":
        return "exit"
    else:
        print("Invalid input, try again")
        pick_input(prompt)

startClient("localhost", 3000, PROMPT)
