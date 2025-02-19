from socket import *

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
    # starter klient socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    try:
        # sender korrekt input til serverSocket og får tilbake en respons
        choice = pick_input(prompt)
        clientSocket.send(choice.encode())
        serverResponse = clientSocket.recv(1024)
        if choice == "exit":
            return
        print(f"Fra tjener: {serverResponse.decode()}")
    finally:
        # Lukker klient socket etter at en respons er sendt
        clientSocket.close()
        print("Connection closed.")

def pick_input(prompt):
    # velger rett innput via prom
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
        print("Ugyldig input, prøv igjen!")
        return pick_input(prompt)

startClient("localhost", 3000, PROMPT)
