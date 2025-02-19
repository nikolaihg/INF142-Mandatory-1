from socket import *
import json

# "database"
database = {
    100 : {
    "tittel": "Hva skal jeg ha til middag?",
    "alternativ": {
        "Pølse": 0, "Hamburger": 0, "PIzza": 0
        }
    }  
}

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
                # Sjekker om melding inneholder ett mellomrom, siden dette betyr at den også inneholder en problemID
                elif " " in message:  
                    command, problemID = message.split(" ", 1)
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