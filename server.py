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

def get_votes():
    # Returnerer databasen som JSON-streng, i henhold til valg 2 slik som spesifiser i oppgaveteksten.
    return json.dumps(database, indent=2, ensure_ascii=False)

def get_problem(problemID): 
    # Returnerer tittel og alternativer for et gitt problemID, men ikke selve ID-en.
    problemID = int(problemID)  # Konverter til heltall
    if problemID in database:
        problem = database[problemID]
        return json.dumps({
            "tittel": problem["tittel"],
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
                elif message == "1":
                    response = f"Respons fra tjener: {message}"
                    connectionSocket.send(response.encode())
                # Hvis klient velger alternativ 2, send databasen
                elif message == "2":
                    response = f"\n{get_votes()}"
                    connectionSocket.send(response.encode())
                # Sjekker om melding inneholder ett mellomrom, siden dette betyr at den også inneholder en problemID
                elif " " in message:  
                    parts = message.split(" ", 2)  # Split into maks 3 deler
                    command = parts[0]
                    problemID = parts[1]

                    # Hvis kommando er "3" (hente problem)
                    if command == "3":
                        response = f"\n{get_problem(problemID)}"
                        connectionSocket.send(response.encode())
                    # Hvis kommando er "5" (stemming)
                    if command == "5" and len(parts) == 3:
                        vote = parts[2]
                        response = f"Stemme mottatt: {vote} for problem {problemID}"
                        connectionSocket.send(response.encode())
                    else:
                        response = f"kommando: {command}, problemID: {problemID}"
                        connectionSocket.send(response.encode())
                # Standard respons for "enkel kommando"
                elif message:
                    # melding som sendes til klient
                    response = f"Respons fra tjener: {message}"
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