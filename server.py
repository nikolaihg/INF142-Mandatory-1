from socket import *
import json

# "database"
database = {
    100 : {
    "tittel": "Hva skal jeg ha til middag?",
    "alternativ": {
        "Pølse": 0, "Hamburger": 0, "Pizza": 0
        }
    },
    101 : {
    "tittel": "Når skal jeg stå opp",
    "alternativ": {
        "13:00": 0, "07:00": 0, "09:00": 0
        }
    }   
}

# Post problem (valg 1. i client.py)
def post_problem(problemID, tittel, alternatives):
    """Legger til et nytt problem i databasen."""
    problemID = int(problemID)
    # Sjekker om problemID allerede finnes
    if problemID in database:
        return f"Feil: Problem med ID {problemID} finnes allerede."
    # Konverterer alternativer fra streng til dictionary med stemmetall 0
    alt_dict = {alt.strip(): 0 for alt in alternatives.split(",")}
    # Legger til det nye problemet i databasen
    database[problemID] = {
        "tittel": tittel,
        "alternativ": alt_dict
    }
    return f"Problem {problemID} lagt til: {tittel} med alternativer {list(alt_dict.keys())}."

# Spør etter problem (valg 2. i client.py)
def get_problem(problemID): 
    """Returnerer tittel og alternativer for et gitt problemID"""
    problemID = int(problemID)
    if problemID in database:
        problem = database[problemID]
        return json.dumps({
            "tittel": problem["tittel"],
            "alternativ": problem["alternativ"]
        }, indent=2, ensure_ascii=False)
    return f"Feil: Problem med ID {problemID} finnes ikke."

# Vis en problemformulering (valg 3. i client.py)
def get_votes():
    """Returnerer databasen som JSON-streng, i henhold til valg 2 slik som spesifiser i oppgaveteksten."""
    return json.dumps(database, indent=2, ensure_ascii=False)

# Vis alternativer (valg 4. i client.py)
def show_options(problemID):
    """Returnerer alternativene og stemmetall for gitt problemID."""
    problemID = int(problemID)
    if problemID in database:
        return json.dumps(database[problemID]["alternativ"], indent=2, ensure_ascii=False)
    return f"Feil: Problem med ID {problemID} finnes ikke."

# Stem på alternativ (valg 5. i client.py)
def vote(problemID, vote):
    """Øker stemmetallet for alternativ for problem gitt ved problemID."""
    problemID = int(problemID)
    if problemID in database:
        if vote in database[problemID]["alternativ"]:
            database[problemID]["alternativ"][vote] += 1
            return f"Stemme registrert: '{vote}' for problem {problemID}."
        else:
            return f"Feil: '{vote}' er ikke et gyldig alternativ for problem {problemID}."
    return f"Feil: Problem med ID {problemID} finnes ikke."

# Vis stemmer på et problem (valg 6. i client.py)
def show_votes(problemID):
    """Returnerer stemmetall for et gitt problemID."""
    problemID = int(problemID)
    if problemID in database:
        problem = database[problemID]
        return json.dumps({
            "alternativ": problem["alternativ"]
        }, indent=2, ensure_ascii=False)
    return f"Feil: Problem med ID {problemID} finnes ikke."

def start_server(serverPort):
    # starter tjener socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Tjener startet!")

    try:
        while True:
            # kobler til klient
            connectionSocket, addr = serverSocket.accept()
            print(f"Koblet til {addr}")
            
            try:
                # mottat melding fra klient
                message = connectionSocket.recv(1024).decode()
                print(f"Fra klient: {message}")
                # Hvis melding fra klient er "exit", så sender man ikke noe respons
                if message.lower() == "exit":
                    print(f"kommando: {message} -> kobling stengt")
                    pass 
                # Hvis klient velger alternativ 2, send databasen
                elif message == "2":
                    response = f"\n{get_votes()}"
                    connectionSocket.send(response.encode())
                # Sjekker om melding inneholder ett mellomrom, siden dette betyr at den også inneholder en problemID / og kanskje stemme
                elif " " in message:  
                    parts = message.split(" ", 3)  # Split into maks 4 deler
                    command = parts[0]
                    problemID = parts[1]
                    # Legge til nytt problem (1 problemID tittel alternativer)
                    if command == "1" and len(parts) == 4:
                        # Jeg har ikke klart å implementer denne enda
                    # Hvis kommando er "3" (hente problem)
                    if command == "3":
                        response = f"\n{get_problem(problemID)}"
                        connectionSocket.send(response.encode())
                    # Hvis kommando er "4" (vise alternativer/stemmer)
                    elif command == "4":
                        response = f"\n{show_options(problemID)}"
                        connectionSocket.send(response.encode())
                    # Hvis kommando er "5" (stemming)
                    elif command == "5" and len(parts) == 3:
                        choice = parts[2]
                        vote(problemID, choice)
                        print(database)
                    # Hvis kommando er "6" (vise stemmer)
                    elif command == "6":
                        response = f"\n{show_votes(problemID)}"
                        connectionSocket.send(response.encode())
                # Standard respons hvis kommando som blir sendt er feil
                elif message:
                    response = f"Send kommando {message} ble ikke parset"
                    connectionSocket.send(response.encode())
            except Exception as e:
                print(f"Error: {e}")
            finally:
                connectionSocket.close()
                print("Tilkobling stengt")
    except KeyboardInterrupt:
        # tjener stenges ved ctrl-c
        print("\nTjener stenges...")
    finally:
        serverSocket.close()
        print("Tjener socket stengt.")

start_server(3000)