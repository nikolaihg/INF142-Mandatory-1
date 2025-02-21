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

def start_client(serverName: str, serverPort: int, prompt: str):
    """Starter klient socket, tar hånd om brukerinput"""
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    try:
        # sender korrekt input til serverSocket og får tilbake en respons
        choice = get_user_input(prompt)
        clientSocket.send(choice.encode())
        serverResponse = clientSocket.recv(1024)
        if choice == "exit":
            return
        print(f"Fra tjener: {serverResponse.decode()}")
    finally:
        # lukker klient socket etter at en respons er sendt
        clientSocket.close()
        print("Connection closed.")

def get_user_input(prompt: str) -> str:
    """Returnerer en formatert string av brukervalg\n
    For eksempel: "1;200;Hva skal vi gjøre i helgen?; Gå på kino; Spille Spill" for å legge til ett nytt problem
    """
    print(prompt)
    choice = input("Velg handling: ")
    
    if choice == "1":
        problem_id = input("problemID: ")
        title = input("tittel: ")
        alternatives = []
        while True:
            alternative = input("Skriv inn et alternativ (eller 'stop' for å avslutte): ")
            if alternative.lower() == "stop":
                break
            alternatives.append(alternative)
        return f"{choice};{problem_id};{title};{';'.join(alternatives)}"
    elif choice in {"2", "3", "4", "6"}:
        if choice != "2":
            problem_id = input("problemID: ")
            return f"{choice};{problem_id}"
        return choice
    elif choice == "5":
        problem_id = input("problemID: ")
        vote = input("Skriv din stemme: ")
        return f"{choice};{problem_id};{vote}"
    elif choice.lower() == "exit":
        return "exit"
    else:
        print("Ugyldig input, prøv igjen!")
        get_user_input(prompt)

if __name__ == "__main__":
    start_client("localhost", 3000, PROMPT)
