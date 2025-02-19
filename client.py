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
        # lukker klient socket etter at en respons er sendt
        clientSocket.close()
        print("Connection closed.")

def pick_input(prompt):
    # velger rett innput via prompt
    print(prompt)
    choice = input("Velg handling: ")

    if choice == "1":
        print("Skriv inn problem på følgende måte:")
        print('100 : {"tittel": "Hva skal jeg ha til middag?","alternativ": {"Pølse": 0, "Hamburger": 0, "Pizza": 0}}')
        json_string = input()
        return choice + " " + json_string
    elif choice == "2":
        return choice # Format: "2"
    elif choice == "3":
        problemID = input("problemID: ")
        return choice + " " + problemID # Format: "3 problemID"
    elif choice == "4":
        problemID = input("problemID: ")
        return choice + " " + problemID # Format: 4 problemID
    elif choice == "5":  # 
        problemID = input("problemID: ")
        vote = input("Skriv din stemme: ") 
        return choice + " " + problemID + " " + vote  # Format: "5 problemID vote"
    elif choice == "6":
        problemID = input("problemID: ")
        return choice + " " + problemID # Format: "6 problemID"
    elif choice.lower() == "exit":
        return "exit" # Format: "exit"
    else:
        print("Ugyldig input, prøv igjen!")
        return pick_input(prompt)

startClient("localhost", 3000, PROMPT)
