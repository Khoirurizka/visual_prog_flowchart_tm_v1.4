from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

url = "http://127.0.0.2:8000/LLM_message_response"
#url = "https://gai.hucenrotia.ngrok.dev/LLM_message_response"
@app.route('/LLM_reciever_prompt', methods=['POST'])
def receive_string():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid data format'}), 400

        message = data['message']
        print(message)
        post_data = {
            'message': "Ok, I will install the blue wire to the power supply terminal 5.",
            'output_pddl': "\n(find blue_wire)\n(pickup arm1 blue_wire table)\n(insert arm1 blue_wire power_supply_5)\n(putdown arm1 blue_wire power_supply_5)\n(lock arm2 blue_wire power_supply_5)"
            }
        
        response = requests.post(url, json=post_data)
        print(f"Data sent: {response.status_code}, Response: {response.text}")

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=9000)


