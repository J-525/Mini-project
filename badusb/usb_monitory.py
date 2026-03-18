import pyudev
import time
import sus

def monitor_usb(stop_event):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)

    monitor.filter_by(subsystem="input")

    print("Monitoring USB devices...")

    for action, device in monitor:
        
        if stop_event.is_set():
            break

        if action == "add":

            if device.get("ID_INPUT_KEYBOARD") == "1" and device.device_node:
               # print("New keyboard device connected \n")
                #print("Device:", device.device_node)
                
                sus.sus_recent = True
                sus.sus_insert_time = time.time()
                sus.sus_reset_needed = True
                #return device.device_node



'''if __name__ == "__main__":
    try:
        monitor_usb()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")'''