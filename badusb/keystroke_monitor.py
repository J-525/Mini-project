import evdev
from evdev import InputDevice, categorize, ecodes
from select import select
import time 

total_keys=0
backspace_count=0
last_time=None

devices=[]
delays=[]
for path in evdev.list_devices():
    dev=evdev.InputDevice(path)
    if ecodes.EV_KEY in dev.capabilities():
        keys=dev.capabilities()[ecodes.EV_KEY]
        if ecodes.KEY_A in keys and ecodes.KEY_Z in keys:
         devices.append(dev)

devices = {dev.fd: dev for dev in devices}

while True:
    r,w,x=select(devices,[],[])
    for fd in r:
        for event in devices[fd].read():
            if event.type == ecodes.EV_KEY and event.value ==1:
                key_event=categorize(event)

                if key_event.keystate == key_event.key_down:
                    total_keys+=1
                    current_time = time.timestamp()

                    if last_time:
                        delay = current_time - last_time
                        print(delay)
                        print(devices[fd].name)
                        delays.append(delay)
                    last_time = current_time
                    
                    if key_event.keycode == 'KEY_BACKSPACE':
                        backspace_count+=1
                    
    #print(f"Total keys pressed: {total_keys}, Backspace count: {backspace_count}")
