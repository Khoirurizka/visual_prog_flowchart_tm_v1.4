import cv2
import requests
import base64

url_update_screw_diver_capture = "http://localhost:6000/screw_diver_capture"

def capture_image_from_cam():
    # Open a connection to the default camera (usually the first camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    scalled_frame = cv2.resize(frame, (480, 320))
    # Encode the frame into bytes (JPEG format)
    _, img_encoded = cv2.imencode('.jpg', scalled_frame)

    # Convert to bytes for sending
    base64_image = base64.b64encode(img_encoded)
    response = requests.post(url_update_screw_diver_capture, json={"image": base64_image})
    print(f"Server response: {response.text}")

    if ret:
        # Save the captured frame as an image file
        filename = 'captured_image.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as {filename}")
    else:
        print("Error: Failed to capture image.")

    # Release the camera
    cap.release()

if __name__ == "__main__":
    capture_image_from_cam()
