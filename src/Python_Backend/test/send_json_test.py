from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Define the data to be sent
data = {
    'linkDataArray':[
        {'key': '-1s', 'from': -1, 'to': 0},
        {'key': -2, 'from': 0, 'to': 1}, 
        {'key': -3, 'from': 1, 'to': 2},
        {'key': -4, 'from': 2, 'to': 3},
        {'key': '-5s', 'from': -3, 'to': 4},
        {'key': -5, 'from': 3, 'to': 4}, 
        {'key': -6, 'from': 4, 'to': 5}, 
        {'key': '-7e', 'from': 3, 'to': -2}, 
        {'key': '-8e', 'from': 5, 'to': -4}],
    'nodeDataArray':[
    {'key': -1, 'command': 'Start_arm1', 'color': 'lightblue', 'category': 'StartEnd'},
    {'key': -2, 'command': 'End_arm1', 'color': 'lightblue', 'category': 'StartEnd'},
    {'key': -3, 'command': 'Start_arm2', 'color': 'lightblue', 'category': 'StartEnd'},
    {'key': -4, 'command': 'End_arm2', 'color': 'lightblue', 'category': 'StartEnd'},
    {'key': 0, 'command': 'find', 'color': 'white', 'category': 'Process'},
    {'key': 1, 'command': 'pickup', 'color': 'white', 'category': 'Process'},
    {'key': 2, 'command': 'insert', 'color': 'white', 'category': 'Process'},
    {'key': 3, 'command': 'putdown', 'color': 'white', 'category': 'Process'},
    {'key': 4, 'command': 'wait another', 'color': 'white', 'category': 'Process'},
    {'key': 5, 'command': 'lock', 'color': 'white', 'category': 'Process'}]
}

# URL of the Electron app
url = "http://localhost:6000"

# Function to send data automatically
def send_data_to_electron():
    while True:
        try:
            print("p")
            print(data)
            response = requests.post(url, json=data)
            print(f"Data sent: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
        time.sleep(10)  # Wait 10 seconds before sending data again

# Background thread to send data automatically
def start_sending_data():
    thread = threading.Thread(target=send_data_to_electron)
    thread.daemon = True
    thread.start()

@app.route('/')
def home():
    return jsonify({"status": "Flask app running", "message": "Automatic data sending to Electron enabled"})

if __name__ == '__main__':
    start_sending_data()  # Start the background thread
    app.run(port=5000, debug=True)

