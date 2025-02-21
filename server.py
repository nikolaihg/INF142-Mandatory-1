from socket import *
import json

# "database"
database = {
    101 : {
    "tittel": "Når skal jeg stå opp",
    "alternativ": {
        "13:00": 0, "07:00": 0, "09:00": 0
        }
    },
    100 : {
    "tittel": "Hva skal jeg ha til middag?",
    "alternativ": {
        "Pølse": 0, "Hamburger": 0, "Pizza": 0
        }
    },   
}

def parse_input(message):
    """Parses meldingen for valg 1. (brukes bare i valg 1, de andre valgene gjør parsin i handle_input())\n
    Returnerer input som dict()"""
    parts = message.split(";")
    command = parts[0].strip()
    problemID= parts[1].strip()
    title = parts[2].strip()
    options = [option.strip() for option in parts[3:]]

    return {
        "command": command,
        "problem_id": problemID,
        "title": title,
        "options": options
    }

def post_problem(input_string: str, database: dict):
    """Post problem (valg 1. i client.py)\n
    Tar inn ett problem som streng og legger den til i databasen."""
    parsed_data = parse_input(input_string)
    
    problem_id = int(parsed_data["problem_id"])
    title = parsed_data["title"]
    options = parsed_data["options"]
    alternatives = {option: 0 for option in options}

    database[problem_id] = {
        "tittel": title,
        "alternativ": alternatives
    }

def get_problem(problemID: str) -> str: 
    """Spør etter problem (valg 2. i client.py)\n
    Returnerer tittel og alternativer for et gitt problemID"""
    problemID = int(problemID)
    if problemID in database:
        problem = database[problemID]
        return json.dumps({
            "tittel": problem["tittel"],
            "alternativ": problem["alternativ"]
        }, indent=2, ensure_ascii=False)
    return f"Feil: Problem med ID {problemID} finnes ikke."

def get_votes() -> str:
    """Vis en problemformulering (valg 3. i client.py)\n
    Returnerer databasen som JSON-streng, i henhold til valg 2 slik som spesifiser i oppgaveteksten."""
    return json.dumps(database, indent=2, ensure_ascii=False)

def show_options(problemID: str) -> str:
    """Vis alternativer (valg 4. i client.py)\n
    Returnerer alternativene og stemmetall for gitt problemID."""
    problemID = int(problemID)
    if problemID in database:
        return json.dumps(database[problemID]["alternativ"], indent=2, ensure_ascii=False)
    return f"Feil: Problem med ID {problemID} finnes ikke."

def vote(problemID: str, vote: str) -> str:
    """Stem på alternativ (valg 5. i client.py)\n
    Øker stemmetallet for alternativ for problem gitt ved problemID."""
    problemID = int(problemID)
    if problemID in database:
        if vote in database[problemID]["alternativ"]:
            database[problemID]["alternativ"][vote] += 1
            return f"Stemme registrert: '{vote}' for problem {problemID}."
        else:
            return f"Feil: '{vote}' er ikke et gyldig alternativ for problem {problemID}."
    return f"Feil: Problem med ID {problemID} finnes ikke."

def show_votes(problemID: str) -> str:
    """Vis stemmer på et problem (valg 6. i client.py)\n
    Returnerer stemmetall for et gitt problemID."""
    problemID = int(problemID)
    if problemID in database:
        problem = database[problemID]
        return json.dumps({
            "alternativ": problem["alternativ"]
        }, indent=2, ensure_ascii=False)
    return f"Feil: Problem med ID {problemID} finnes ikke."

def handle_response(message: str) -> str :
    """Returnerer korrekt respons utifra melding fra klient"""                
    response = ""
    # Hvis melding fra klient er "exit", så sender man ikke noe respons
    if message.lower() == "exit":
        print(f"kommando: {message}")
        print("Kobling stengt.")
        pass 
    # Hvis melding fra klient starter med "1;" -> legg til problem
    elif message.startswith("1;"):
        post_problem(message, database)
        response = "Problem problem lagt til i databasen."
        print(response)
    # Hvis klient velger alternativ "2;" -> send databasen
    elif message.startswith("2"):
        response = f"\n{get_votes()}"
        print("Viser alle problem til klient.")
    # Sjekker om melding inneholder ";", siden dette betyr at den også inneholder en problemID / og kanskje stemme
    elif ";" in message:  
        parts = message.split(";", 3)  # Splitert melding i maks 4 deler ["kommando", "problemID", "tittel", "alternativ"]
        command = parts[0]
        problemID = parts[1]
        # Hvis kommando er "3" -> hente problem
        if command.startswith("3"):
            response = f"\n{get_problem(problemID)}"
            print(f"Viser problem: {problemID} til klient.")
        # Hvis kommando er "4" -> vise alternativer
        elif command.startswith("4"):
            response = f"\n{show_options(problemID)}"
            print(f"Viser alternativ: {problemID} til klient.")
        # Hvis kommando er "5" -> stemming
        elif command.startswith("5") and len(parts) >= 3:
            choice = parts[2]
            vote(problemID, choice)
            response = f"Stemmer oppdater for problem: {problemID}."
            print(response)
            print(database)
        # Hvis kommando er "6" -> vise stemmer
        elif command.startswith("6"):
            response = f"\n{show_votes(problemID)}"
            print(f"Viser stemmer for {problemID} til klient.")
    # Standard respons hvis kommando som blir sendt er feil
    else:
        response = f"Send kommando {message} ble ikke parset."
    return response

def start_server(serverPort: int):
    """Starter og avslutter tjener socket"""
    # starter tjener socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Tjener startet!")

    try:
        while True:
            # kobler til klient
            connectionSocket, addr = serverSocket.accept()
            print(f"Koblet til {addr}.")
            
            try:
                # mottat melding fra klient
                message = connectionSocket.recv(1024).decode()
                print(f"Fra klient: {message}")
                # velge korrekt handling+respons ut i fra melding
                response = handle_response(message)
                # sende respons til klient
                connectionSocket.send(response.encode())
            except Exception as e:
                print(f"Feil: {e}.")
            finally:
                connectionSocket.close()
                print("Tilkobling stengt.")
    except KeyboardInterrupt:
        # tjener stenges ved ctrl-c
        print("\nTjener stenges...")
    finally:
        serverSocket.close()
        print("Tjener socket stengt.")

if __name__ == "__main__":
    start_server(3000)