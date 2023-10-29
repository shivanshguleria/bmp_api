import time
from bmp280 import BMP280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import requests

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

url = "https://young-paper-8770.fly.dev/post"
while True:
    t = bmp280.get_temperature()
    p = bmp280.get_pressure()
    a = 0
    print("[INFO] Data Generated")
    print('{:05.2f}*C {:05.2f}hPa'.format(t, p))
    p_t, p_p, p_a = 0,0,0
    if p_t != t or p_p != p or p_a != a:
        print("[INFO] Conditions Met")
        payload = {
            't': t,
            'p': p,
            "a": a
        }
        print("[INFO] Payload Generated")
        requests.post(url,json=payload)
        print("[INFO] Data Posted to server")
        try:
            signal(SIGTERM, safe_exit)
            signal(SIGHUP, safe_exit)
            lcd.clear()
            lcd.text("{:05.2f}*C".format(t), 1)
            lcd.text("{:05.2f}*hPa".format(p), 2)
            time.sleep(2)
        except KeyboardInterrupt:
            pass
        p_t, p_a, p_p = t, a, p
    else:
        print("Not")
    time.sleep(1)
