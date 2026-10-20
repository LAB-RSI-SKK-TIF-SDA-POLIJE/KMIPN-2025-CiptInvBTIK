import pigpio

class HardwareController:
    def __init__(self, pan_pin=12, tilt_pin=13, laser_pin=17):
        # Pastikan Anda sudah menjalankan 'sudo pigpiod' di terminal RPi
        self.pi = pigpio.pi()
        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        self.laser_pin = laser_pin
        
        self.pi.set_mode(self.laser_pin, pigpio.OUTPUT)

        # Posisi tengah servo (pulse width 1500)
        self.pan_pw = 1500
        self.tilt_pw = 1500
        self.update_servos()

    def update_servos(self):
        self.pi.set_servo_pulsewidth(self.pan_pin, self.pan_pw)
        self.pi.set_servo_pulsewidth(self.tilt_pin, self.tilt_pw)

    def fire_laser(self, on=True):
        self.pi.write(self.laser_pin, 1 if on else 0)