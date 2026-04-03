from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-api-key'
        return response

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

    response = jsonify(r.json())
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, r.status_code

if __name__ == '__main__':
    app.run()
