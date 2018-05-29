import configparser
from pyA20.gpio import gpio
from pyA20.gpio import port
from datetime import datetime
from datetime import timedelta
from time import sleep
import os
import sys
import signal

lamp = port.PA7
fan = port.PA8
fullspeed = port.PA9

day =   [
        (lamp, 1),
        (fan, 1),
        (fullspeed, 1)
        ]

night = [
        (lamp, 0),
        (fan, 1)
        ]

silent = [
        (fan, 1),
        (fullspeed, 0)
        ]

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'conf.ini'))
DATE_FORMAT = '%H:%M'
sunrise = config['Default']['sunrise']
sunrise = datetime.strptime(sunrise, DATE_FORMAT)
t = datetime.now() - timedelta(days=1)
sunrise = datetime(t.year, t.month, t.day, sunrise.hour, sunrise.minute)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def set_mode(mode):
    gpio.init()
    for param in mode:
        gpio.setcfg(*param)


def main():
    now = datetime.now()
    global sunrise
    daytime = config['Default']['daytime']
    daytime = timedelta(hours=int(daytime))
    sunset = sunrise + daytime
    night_len = timedelta(hours=24) - daytime

    if now > sunrise and now < sunset:
        set_mode(day)

    elif now > sunset and now > sunrise:
        set_mode(night)
        sleep(120)
        set_mode(silent)
        sunrise = sunset + night_len


if __name__ == '__main__':
    killer = GracefulKiller()
    while True:
        main()
        if killer.kill_now:
            break
        sleep(5)

sleep(5)
set_mode(night)
set_mode(silent)
sys.exit(0)
