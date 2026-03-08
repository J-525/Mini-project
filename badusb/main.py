from usb_monitory import monitor_usb
import keystroke_monitor
from threading import Thread,Event

stop_event = Event()

print("Starting USB monitor... ")

usb_thread = Thread(target=monitor_usb, args=(stop_event,), daemon=True)
usb_thread.start()

try:
    keystroke_monitor.main(stop_event)
except KeyboardInterrupt:
    print("Exiting program.")
    stop_event.set()

finally:
    try:
        usb_thread.join(timeout=2) 
    except KeyboardInterrupt:
        pass