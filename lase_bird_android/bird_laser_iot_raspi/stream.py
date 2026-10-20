from flask import Flask, Response
import cv2

app = Flask(__name__)
global_frame = None

def generate_frames():
    global global_frame
    while True:
        if global_frame is not None:
            # Encode frame gambar menjadi JPG
            ret, buffer = cv2.imencode('.jpg', global_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                # Yield format streaming MJPEG
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # URL ini yang akan diakses oleh aplikasi Flutter Anda
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_stream(host='0.0.0.0', port=5000):
    app.run(host=host, port=port, debug=False, use_reloader=False)