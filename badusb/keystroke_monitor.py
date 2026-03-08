import evdev
from evdev import categorize, ecodes
from select import select
import time 
import config
from risk_engine import evaluate_risk
from alert_engine import beep
import sus



def main(stop_event):

    last_time=None
    window_keys = 0
    window_corrections = 0
    last_alert_time = 0

    #check for different keyboard devices
    devices={}
    delays=[]
    for path in evdev.list_devices():
        dev=evdev.InputDevice(path)
        if dev.fd not in devices:
            if ecodes.EV_KEY in dev.capabilities():
                keys=dev.capabilities()[ecodes.EV_KEY]
                if ecodes.KEY_A in keys and ecodes.KEY_Z in keys:
                    devices[dev.fd]=dev
                    print("new device:",dev.name)

    #devices = {dev.fd: dev for dev in devices}


    #check for key events from all tinput devices

    while not stop_event.is_set():
        r,w,x=select(devices.keys(),[],[],1)
        
        for fd in r:
            try:
                for event in devices[fd].read():
                    if event.type == ecodes.EV_KEY and event.value ==1:
                        key_event=categorize(event)

                        if key_event.keystate == key_event.key_down:
                            window_keys += 1
                            current_time = event.timestamp()

                            if last_time is not None:
                                delay = current_time - last_time
                                #print(delay)
                                #print(devices[fd].name)
                                delays.append(delay)
                            last_time = current_time
                            
                        #check for backspace or delete key to count corrections
                            #if sus.sus_recent and (time.time() - sus.sus_insert_time < 10):
                            #    print("Suspected BadUSB device detected.")
                            #    sus.is_sus=True
                            #else:
                            #    sus.is_sus=False

                            sus.is_sus = sus.sus_recent and (time.time() - sus.sus_insert_time < 10)
                                

                            if key_event.keycode in ('KEY_BACKSPACE', 'KEY_DELETE'):
                                window_corrections += 1
                            
                            

                            if len(delays) > config.WINDOW_SIZE:
                                delays.pop(0)
                            #print("Current window size:", len(delays))
                            if len(delays) == config.WINDOW_SIZE:
                                risk, alert = evaluate_risk(delays, window_keys, window_corrections)
                                #print(f"Risk Level: {risk}")
                                #print(f"Alert: {alert}")

                                #alerts user
                                if sus.is_sus:
                                    risk = min(risk + 3, 10)

                                alert = risk >= config.RISK_THRESHOLD

                                if alert and (time.time() - last_alert_time > 5):
                                    #print("Potential automated input detected! Risk Level:", risk)
                                    last_alert_time = time.time()
                                    #print(last_alert_time)
                                    beep(risk)

                                    #delays.clear()
                                    window_keys = 0
                                    window_corrections = 0
            except OSError:
                print(f"Device {devices[fd].name} disconnected.")
                del devices[fd]
if __name__ == "__main__":
    main()