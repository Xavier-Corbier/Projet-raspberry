# coding: utf-8

from driverLCD import *
from driverBouton import *
from driverRelais import *
from driverLED import *
from driverBuzzer import *
import time

# Main

initBuzzer()
setValeurBuzzer(1)
time.sleep(1)
setValeurBuzzer(0)
