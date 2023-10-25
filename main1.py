
import Adafruit_BMP.BMP085 as BMP085
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import requests
lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

url = "https://bmp-api-8jll.onrender.com/danger"
while True:
    sensor = BMP085.BMP085()
    t = 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())
    p = '{0:0.2f} Pa'.format(sensor.read_pressure())
    a = '{0:0.2f} m'.format(sensor.read_altitude())
    print(t+" "+p+" "+ a)
    p_t, p_p, p_a = 0,0,0
    if p_t != t or p_p != p or p_a != a:
            
        payload = {
            't': t,
            'p': p,
            "a": a
        }
        requests.post(url,json=payload)
        try:
            signal(SIGTERM, safe_exit)
            signal(SIGHUP, safe_exit)
            lcd.text(f"Temprature {a}", 1)
            lcd.text(f"Pressure {p}", 2)
            pause()
        except KeyboardInterrupt:
            pass
        finally:
            lcd.clear()
        p_t, p_a, p_p = t, a, p
    time.sleep(3)