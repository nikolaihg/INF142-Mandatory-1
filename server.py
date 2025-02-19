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
    print("Server has started!")

    try:
        while True:
            # kobler til klient
            connectionSocket, addr = serverSocket.accept()
            print(f"Connected to {addr}")
            
            try:
                # mottat melding fra klient
                message = connectionSocket.recv(1024).decode()
                if message:
                    print(f"From client: {message}")
                    # melding som sendes til klient
                    response = f"Respons fra server: {message}"
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