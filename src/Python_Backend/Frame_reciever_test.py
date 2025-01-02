import cv2
import requests
import numpy as np
from flask import Flask, Response, stream_with_context

# Flask application to receive and serve frames
app = Flask(__name__)

# Route to receive video stream
@app.route('/receive_frame', methods=['POST'])
def video_feed():
    def generate():
        while True:
            yield request.stream.read()  # Read the stream as it comes

    return Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=frame')


# Displaying the received frames using OpenCV
def display_video_stream(url):
    # Sending a GET request to the video stream
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        print("Receiving video stream...")
        byte_data = b""
        for chunk in response.iter_content(chunk_size=1024):
            byte_data += chunk
            a = byte_data.find(b'\xff\xd8')  # Start of JPEG
            b = byte_data.find(b'\xff\xd9')  # End of JPEG

            if a != -1 and b != -1:
                jpg_data = byte_data[a:b+2]  # Extract complete JPEG image
                byte_data = byte_data[b+2:]  # Remove the used bytes from buffer

                frame = cv2.imdecode(np.frombuffer(jpg_data, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("Video Stream", frame)

                if cv2.waitKey(1) == 27:  # Press 'ESC' to quit
                    break
    else:
        print(f"Failed to connect: {response.status_code}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Run the Flask server for receiving video feed
    app.run(host='127.0.0.2', port=5000)
