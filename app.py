from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_command():
    data = request.json
    command = data.get('command')
    url = data.get('url')
    username = data.get('username')
    room_id = data.get('room_id')
    
    if not (url or username or room_id):
        return jsonify({"error": "Missing URL, username, or room ID. Please provide one of these parameters."}), 400
    
    if command:
        try:
            full_command = f"{command} -url {url} -user {username} -room_id {room_id}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return jsonify({"output": result.stdout, "error": result.stderr}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No command provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

