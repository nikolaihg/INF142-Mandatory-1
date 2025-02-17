from socket import *
import json

# "database"
database = {
    100: {
        "title": "Favorite programming language?",
        "options": {"Python": 0, "Java": 0, "C++": 0}
    }
}

def show_votes(problem_id):
    if problem_id in database:
        return json.dumps(database[problem_id].get("options", {}))
    return f"Problem ID {problem_id} not found."

def show_problem(problem_ID):
    if problem_ID in database:
        return json.dumps(database[problem_ID])
    return f"Problem ID {problem_ID} not found."

def show_problems():
    return json.dumps({k: v["title"] for k, v in database.items()})

def handle_client_input(setning):
    if setning == "2":
        return show_problems()
    elif setning.startswith("valg: 3"):
        parts = setning.split()
        if len(parts) == 3:
            problem_id = int(parts[2])
            return show_problem(problem_id)
        else:
            return "Invalid request format."
    else:
        return "Unknown command."

def start_server(serverPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Server has started!")

    # try:
    #     while True:
    #         connectionSocket, addr = serverSocket.accept()
    #         try:
    #             setning = connectionSocket.recv(1024).decode()
    #             print(f"From client: {setning}")
    #             storeBokstaver = setning.upper()
    #             connectionSocket.send(storeBokstaver.encode())
    #         finally:
    #             connectionSocket.close()
    #             print("Connection socket closed")
    # except KeyboardInterrupt:
    #     print("\nServer is shutting down...")
    # finally:
    #     close_server(serverSocket)

    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            print(f"Connected to {addr}")
            try:
                while True:
                    setning = connectionSocket.recv(1024).decode()
                    if not setning or setning.lower() == "exit":
                        break

                    print(f"From client: {setning}")
                    response = handle_client_input(setning)
                    connectionSocket.send(response.encode())

            except Exception as e:
                print(f"Error: {e}")
            finally:
                connectionSocket.close()
                print("Connection socket closed")
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        serverSocket.close()
        print("Server socket closed.")

def close_server(serverSocket):
    serverSocket.close()
    print("Server socket closed.")

start_server(3000)
