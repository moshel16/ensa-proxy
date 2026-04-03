from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-api-key'
    return response

@app.route('/api/proxy', methods=['GET', 'POST', 'OPTIONS'])
def proxy():
    if request.method in ['OPTIONS', 'GET']:
        return make_response('OK', 200)

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
        return response

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run()
