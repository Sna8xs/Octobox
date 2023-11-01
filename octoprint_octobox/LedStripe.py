import RPi.GPIO as GPIO
import threading
import time

class LedStripe:
    def __init__(self, red_pin, green_pin, blue_pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.__failed_bool = False

    def off(self):
        self.__failed_bool = False
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def print_done(self):
        self.off()
        GPIO.output(self.green_pin, GPIO.HIGH)

    def print_failed(self):
        self.off()
        x = threading.Thread(target=self.__failed, args=(1,))
        x.start()

    def __failed(self, num):
        self.__failed_bool = True
        try:
            p = GPIO.PWM(self.red_pin, 100)
            p.start(0)
            while self.__failed_bool:
                for dc in range(0, 101, 5):
                    p.ChangeDutyCycle(dc)
                    time.sleep(0.1)
                    if not self.__failed_bool:
                        break
                if not self.__failed_bool:
                    break
                for dc in range(100, -1, -5):
                    p.ChangeDutyCycle(dc)
                    time.sleep(0.1)
                    if not self.__failed_bool:
                        break
        finally:
            p.stop()
            GPIO.cleanup()

