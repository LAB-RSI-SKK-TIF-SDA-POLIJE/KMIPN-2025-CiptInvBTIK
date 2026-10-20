class Tracker:
    def __init__(self, frame_width=640, frame_height=480):
        self.center_x = frame_width // 2
        self.center_y = frame_height // 2
        self.pan_step = 10   # Kecepatan pergerakan servo horizontal
        self.tilt_step = 10  # Kecepatan pergerakan servo vertikal
        self.threshold = 40  # Toleransi target (piksel) untuk menembakkan laser

    def calculate_movement(self, bird_center, current_pan, current_tilt):
        if not bird_center:
            return current_pan, current_tilt, False

        bx, by = bird_center
        new_pan = current_pan
        new_tilt = current_tilt
        fire_laser = False

        # Hitung sumbu X (Pan) - asumsikan servo bergerak terbalik, sesuaikan +/- jika salah arah
        if bx < (self.center_x - self.threshold):
            new_pan += self.pan_step  # Kamera harus ke kiri
        elif bx > (self.center_x + self.threshold):
            new_pan -= self.pan_step  # Kamera harus ke kanan

        # Hitung sumbu Y (Tilt)
        if by < (self.center_y - self.threshold):
            new_tilt -= self.tilt_step  # Kamera harus ke atas
        elif by > (self.center_y + self.threshold):
            new_tilt += self.tilt_step  # Kamera harus ke bawah

        # Batas aman Pulse Width servo (biasanya 500 sampai 2500)
        new_pan = max(500, min(2500, new_pan))
        new_tilt = max(500, min(2500, new_tilt))

        # Jika burung sudah berada tepat di tengah frame, aktifkan laser
        if abs(bx - self.center_x) <= self.threshold and abs(by - self.center_y) <= self.threshold:
            fire_laser = True

        return new_pan, new_tilt, fire_laser