from flask import Flask, request, jsonify
from datetime import datetime
import requests
import base64
import os
import cv2
import numpy as np
app = Flask(__name__)
# Directory to save received images
SAVE_DIR = "received_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

@app.route('/AI_reciever_prompt_image', methods=['POST'])
def receive_string():
    try:
        ### recieving data
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        image_data = base64.b64decode(data['frame_screw_driver'])

        # Save the image
        #image_path = os.path.join(SAVE_DIR, 'received_image.jpg')
        #with open(image_path, 'wb') as image_file:
        #    image_file.write(image_data)
        np_arr = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #cv2.imshow('Frame - Screw Driver', image)
        #cv2.waitKey(0)  # Wait for a key press to close the window
        #cv2.destroyAllWindows()

        ### sending data
        _, img_encoded = cv2.imencode('.jpg', image)
        base64_image = base64.b64encode(img_encoded).decode('utf-8') 
        message = data['message']
        print(message)
        post_data = {
            'message': "Ok, I will install the blue wire to the power supply terminal 5.",
            'output_pddl': "\n(find blue_wire)\n(pickup arm1 blue_wire table)\n(insert arm1 blue_wire power_supply_5)\n(putdown arm1 blue_wire power_supply_5)\n(lock arm2 blue_wire power_supply_5)",
            'vlm_frame': base64_image
            }

        return jsonify({'status': 'success', "data": post_data}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=9000)


