import cv2
import threading
from flask import Flask, Response

app = Flask(__name__)

frame = None  # Shared frame between threads
frame_lock = threading.Lock()  # Lock for thread-safe access to the frame

class CameraThread:
    def __init__(self, src=0):
        self.src = src  # Camera source, default is 0 for the primary camera
        self.cap = cv2.VideoCapture(self.src)
        self.running = False
        self.thread = threading.Thread(target=self.update, daemon=True)

    def start(self):
        if not self.cap.isOpened():
            raise Exception("Camera could not be opened")
        self.running = True
        self.thread.start()

    def update(self):
        global frame
        while self.running:
            ret, new_frame = self.cap.read()
            if not ret:
                break
            with frame_lock:
                frame = new_frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()

def generate_frames():
    global frame
    while True:
        with frame_lock:
            if frame is None:
                continue  # Skip iteration if no frame is available yet
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.route('/bev_frame_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_camera_UI(cam):
    while True:
        with frame_lock:
            if frame is not None:
                cv2.imshow("Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = CameraThread(src=0)
    cam.start()
    threading.Thread(target=lambda: app.run(host='127.0.0.1', port=5001, debug=False), daemon=True).start()

    try:
        run_camera_UI(cam)
    finally:
        cam.stop()
        cv2.destroyAllWindows()
