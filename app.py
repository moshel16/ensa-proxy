from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-api-key'
    return response

@app.route('/api/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        return add_cors(make_response('', 204))

    try:
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

        response = make_response(r.content, r.status_code)
        response.headers['Content-Type'] = 'application/json'
        return add_cors(response)

    except Exception as e:
        response = make_response(jsonify({'error': str(e)}), 500)
        return add_cors(response)

if __name__ == '__main__':
    app.run()
