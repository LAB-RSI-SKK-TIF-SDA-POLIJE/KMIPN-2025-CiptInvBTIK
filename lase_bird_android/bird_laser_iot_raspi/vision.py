from ultralytics import YOLO
import cv2

class VisionSystem:
    def __init__(self):
        # YOLO akan otomatis mendownload yolov8n.pt jika belum ada
        self.model = YOLO('yolov8n.pt') 
        self.bird_class_id = 16  # ID COCO untuk burung

    def detect(self, frame):
        # Jalankan inferensi khusus untuk kelas burung
        results = self.model(frame, classes=[self.bird_class_id], verbose=False)
        bird_center = None

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Dapatkan koordinat bounding box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Gambar kotak di sekitar burung (untuk visual streaming)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                # Hitung titik pusat burung
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                bird_center = (cx, cy)

                # Gambar titik target di tengah burung
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                
                # Asumsi: kunci target pada burung pertama yang terdeteksi
                break 

        return frame, bird_center