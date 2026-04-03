
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        return '', 204

    api_key = request.headers.get('x-api-key')
    body = request.json
    body['stream'] = False

    r = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        },
        json=body,
        timeout=120
    )

    return jsonify(r.json()), r.status_code

if __name__ == '__main__':
    app.run()
