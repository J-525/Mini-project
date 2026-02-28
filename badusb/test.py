from pynput.keyboard import Controller
import time

keyboard = Controller()

payload = "hello this is automated typing\n"

for char in payload:
    keyboard.type(char)
    time.sleep(0.002)   # VERY FAST