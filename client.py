from socket import *

PROMPT = """
1. (POST problem) Legg til problem.
2. Vis alle eksisterende problemer.
3. Vis problem: (problemID).
4. Vis alternativ: (problemID).
5. Stem på alternativ: (problemID).
6. Vis stemmer: (problemID).
7. Skriv 'exit' for å avslutte.
"""

def startClient(serverName: str, serverPort: int, prompt: str):
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
        # lukker klient socket etter at en respons er sendt
        clientSocket.close()
        print("Connection closed.")

def pick_input(prompt: str) -> str:
    print(prompt)
    choice = input("Velg handling: ")
    if choice == "1":
        problemID = input("problemID: ")
        tittel = input("tittel: ")
        alternatives = []
        while True:
            alternative = input("Skriv inn et alternativ (eller 'stop' for å avslutte): ")
            if alternative.lower() == "stop":
                break
            alternatives.append(alternative)
        return choice + ";" + problemID + ";" + tittel + ";" + ";".join(alternatives)
    elif choice == "2":
        return choice
    elif choice == "3":
        problemID = input("problemID: ")
        return choice + ";" + problemID
    elif choice == "4":
        problemID = input("problemID: ")
        return choice + ";" + problemID 
    elif choice == "5":  # 
        problemID = input("problemID: ")
        vote = input("Skriv din stemme: ") 
        return choice + ";" + problemID + ";" + vote
    elif choice == "6":
        problemID = input("problemID: ")
        return choice + ";" + problemID
    elif choice.lower() == "exit":
        return "exit"
    else:
        print("Ugyldig input, prøv igjen!")
        return pick_input(prompt)

startClient("localhost", 3000, PROMPT)
