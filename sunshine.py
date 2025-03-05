import configparser
import logging
import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
from datetime import time
from time import sleep
import sys

logging.basicConfig(level=logging.INFO)
GPIO.setmode(GPIO.BCM)

# init Capacitors for fan speed control
cap_2 = 17
cap_1a = 27
cap_1b = 22
cap_1c = 23
cap_05 = 24
bypass = 25
GPIO.setup(cap_2,  GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cap_1a, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cap_1b, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cap_1c, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cap_05, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(bypass, GPIO.OUT, initial=GPIO.HIGH)

# Init misc (additional) channels
misc_1 = 5
misc_2 = 6
GPIO.setup(misc_1, GPIO.OUT, initial=GPIO.HIGH) # Misc 1
GPIO.setup(misc_2, GPIO.OUT, initial=GPIO.HIGH) # Misc 2

# Lamp
lamp = 16
GPIO.setup(lamp, GPIO.OUT, initial=GPIO.LOW) # Lamp
logging.info('GPIO init complete')

# Read config
config = configparser.ConfigParser()
config.read(sys.argv[1])
sunrise = config['Default']['sunrise']
sunrise = datetime.strptime(sunrise, '%H:%M')
t = datetime.now() - timedelta(days=1)
sunrise = datetime(t.year, t.month, t.day, sunrise.hour, sunrise.minute)
logging.info('Config read complete')
logging.info('sunrise = %s' % sunrise)

def set_fan_speed(level):
    # Levels 0 to 10
    # 0 is Off
    # 10 is bypass
    
    ch_available = [cap_2, cap_1a, cap_1b, cap_1c, cap_05, bypass]
    fan_speed_levels = [ [],
                         [cap_1a],
                         [cap_1a, cap_05],
                         [cap_2],
                         [cap_2, cap_05],
                         [cap_2, cap_1a],
                         [cap_2, cap_1a, cap_05],
                         [cap_2, cap_1a, cap_1b],
                         [cap_2, cap_1a, cap_1b, cap_05],
                         [cap_2, cap_1a, cap_1b, cap_1c],
                         [bypass]
                        ]

    for channel in set(ch_available) - set(fan_speed_levels[level]):
        GPIO.output(channel, GPIO.HIGH)

    for channel in fan_speed_levels[level]:
        GPIO.output(channel, GPIO.LOW)

def main():
    now = datetime.now()
    global sunrise
    daytime = config['Default']['daytime']
    daytime = timedelta(hours=int(daytime))
    sunset = sunrise + daytime
    night_len = timedelta(hours=24) - daytime
    logging.info('daytime = %s ' % daytime)
    logging.info('sunset = %s ' % sunset)
    logging.info('night_len = %s ' % night_len)

    if now > sunrise and now < sunset:
        logging.info('It is Day now')
        GPIO.output(lamp, GPIO.HIGH)
        with open('/opt/fan_speed_day') as f:
            fan_speed_day = int(f.read())
        set_fan_speed(fan_speed_day)
        logging.info('fan_speed = %s' % fan_speed_day)

    elif now > sunset and now > sunrise:
        logging.info('It is Night now')
        GPIO.output(lamp, GPIO.LOW)
        with open('/opt/fan_speed_night') as f:
            fan_speed_night = int(f.read())
        set_fan_speed(fan_speed_night)
        logging.info('fan_speed = %s' % fan_speed_night)
        sunrise = sunset + night_len
        logging.info('sunrise = %s' % sunrise)

    sleep(15)

if __name__ == '__main__':
    while True:
        main()

logging.info('Stopping...')
logging.info('fan_speed = %s' % fan_speed_night)
GPIO.output(lamp, GPIO.LOW)
with open('/opt/fan_speed_night') as f:
    fan_speed_night = int(f.read())
set_fan_speed(fan_speed_night)
sunrise = sunset + night_len
sys.exit(0)