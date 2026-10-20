import cv2
import threading
from vision import VisionSystem
from tracker import Tracker
from hardware import HardwareController
import stream

def main():
    # 1. Setup komponen
    hw = HardwareController(pan_pin=12, tilt_pin=13, laser_pin=17)
    vision = VisionSystem()
    tracker = Tracker(frame_width=640, frame_height=480)
    
    # 2. Buka kamera (Coba ubah ke 1 atau 2 jika Raspberry Pi Camera tidak terdeteksi di 0)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 3. Jalankan server streaming di background thread
    threading.Thread(target=stream.start_stream, daemon=True).start()
    print("Sistem aktif! Streaming tersedia di http://<IP_RASPBERRY_PI>:5000/video_feed")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Gagal membaca kamera!")
                break

            # A. Deteksi Burung
            annotated_frame, bird_center = vision.detect(frame)

            # B. Hitung pergerakan
            hw.pan_pw, hw.tilt_pw, fire = tracker.calculate_movement(
                bird_center, hw.pan_pw, hw.tilt_pw
            )

            # C. Gerakkan Hardware
            hw.update_servos()
            hw.fire_laser(fire)

            # D. Kirim gambar ke web/Flutter
            stream.global_frame = annotated_frame

    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna.")
    finally:
        cap.release()
        hw.fire_laser(False) # Matikan laser untuk keamanan
        hw.pi.stop()         # Tutup koneksi pigpio

if __name__ == "__main__":
    main()