import pyudev
import datetime

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("usb_security_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='hid')

    log_event("SYSTEM START: Monitoring HID Subsystem for BadUSB threats...")

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            # Extracting deep metadata
            vid = device.get('ID_VENDOR_ID', 'UNKNOWN')
            pid = device.get('ID_MODEL_ID', 'UNKNOWN')
            serial = device.get('ID_SERIAL_SHORT', 'NO_SERIAL')
            product = device.get('ID_MODEL', 'Generic HID')
            
            log_event(f"ALERT: New HID Device Detected!")
            log_event(f"    Product: {product} | VID: {vid} | PID: {pid}")
            log_event(f"    Serial:  {serial}")
            
            # This is the 'Integration' step for Week 3
            if serial == 'NO_SERIAL' or vid == '80ee': # 80ee is VirtualBox
                log_event("    WARNING: Device lacks serial or is virtual. Flagging for Module 3...")
            else:
                log_event("    Notice: Standard device detected.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_event("SYSTEM SHUTDOWN: Monitor stopped by user.")

'''import pyudev


def monitor_usb():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)

    monitor.filter_by(subsystem="input")

    print("Monitoring USB devices...")

    for device in monitor:
        if device.action == "add":

            if device.get("ID_INPUT_KEYBOARD") == "1":
                print("\n⚠ New keyboard device connected")
                print("Device:", device.device_node)
'''
