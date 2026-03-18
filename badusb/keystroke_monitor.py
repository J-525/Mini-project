import evdev
from evdev import categorize, ecodes
from select import select
import time 
import config
from risk_engine import evaluate_risk
from alert_engine import beep
import sus
from logger import log_alert



def main(stop_event):

    last_time=None
    window_keys = 0
    window_corrections = 0
    last_alert_time = 0
    devices={}
    delays=[]
    
    #check for key events from all tinput devices
    try:
        while not stop_event.is_set():

            if sus.sus_reset_needed:
                        delays.clear()
                        window_keys = 0
                        window_corrections = 0
                        sus.sus_reset_needed = False
                        last_time = None 
            
            #check for different keyboard devices
            for path in evdev.list_devices():
                dev=evdev.InputDevice(path)
                if dev.path not in devices:
                    if ecodes.EV_KEY in dev.capabilities():
                        keys=dev.capabilities()[ecodes.EV_KEY]
                        if ecodes.KEY_A in keys and ecodes.KEY_Z in keys:
                            devices[dev.path]=dev
                            print("new device:",dev.name)
            
            
            
            sus.is_sus = sus.sus_recent and (time.time() - sus.sus_insert_time < 10)
            r,w,x=select([dev.fd for dev in devices.values()],[],[],1)
            fd_map = {dev.fd: dev for dev in devices.values()}
        
            for fd in r:
                dev=fd_map.get(fd)
                if not dev:
                    continue

                try:
                    for event in dev.read():

                        if event.type == ecodes.EV_KEY and event.value ==1:
                            key_event=categorize(event)

                            if key_event.keystate == key_event.key_down:
                                window_keys += 1
                                current_time = event.timestamp()

                                if last_time is not None:
                                    delay = current_time - last_time
                                    if delay > 0:
                                        delays.append(delay)
                                    #print(delay)
                                    #print(devices[fd].name)

                                last_time = current_time
                                    
                                #check for backspace or delete key to count corrections
                                    #if sus.sus_recent and (time.time() - sus.sus_insert_time < 10):
                                    #    print("Suspected BadUSB device detected.")
                                    #    sus.is_sus=True
                                    #else:
                                    #    sus.is_sus=False

                                if key_event.keycode in ('KEY_BACKSPACE', 'KEY_DELETE'):
                                    window_corrections += 1                                

                                if len(delays) > config.WINDOW_SIZE:
                                    delays.pop(0)
                                    #print("Current window size:", len(delays))
                                    

                                if len(delays) == config.WINDOW_SIZE:
                                    #print(delays,window_keys,window_corrections)
                                    risk, alert = evaluate_risk(delays, window_keys, window_corrections)
                                    #print(f"Risk Level: {risk}")
                                    #print(f"Alert: {alert}")

                                    #alerts user
                                    if sus.is_sus:
                                        #print(risk)
                                        risk += 5
                                        risk=min(risk,220)

                                    alert = risk >= config.RISK_THRESHOLD

                                    if alert and (time.time() - last_alert_time > 1):
                                        #print("Potential automated input detected! Risk Level:", risk)
                                        last_alert_time = time.time()
                                        #print(last_alert_time)
                                        message = f"BadUSB detected | Risk: {risk}"
                                        log_alert(message) 
                                        beep(risk)

                                    delays.clear()
                                    window_keys = 0
                                    window_corrections = 0
                except OSError:
                    print(f"Device {dev.name} disconnected.")
                    del devices[dev.path]
    except KeyboardInterrupt:
        pass
    finally:
        for dev in devices.values():
            try:
                dev.close()
            except KeyboardInterrupt:
                pass
if __name__ == "__main__":
    from threading import Event
    main(Event())