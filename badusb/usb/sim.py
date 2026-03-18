import pyudev
import subprocess
import time

TARGET_DEVICE = "YICHIP Wireless Device"

# Track already triggered devices
triggered_devices = set()

def simulate():
    print("[SIMULATOR] Starting safe BadUSB simulation...")

    payloads = [
        "echo BADUSB_TEST\n",
        "whoami\n",
        "echo harmless_attack\n"
    ]

    for cmd in payloads:
        # Send full command (more reliable than char-by-char)
        subprocess.run(["ydotool", "type", "--key-delay", "1", cmd])
        time.sleep(0.3)


def monitor_and_trigger():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)

    monitor.filter_by(subsystem="input")  # ✅ fixed typo

    print("[SIMULATOR] Waiting for target device...")

    for action, device in monitor:
        if action != "add":
            continue

        name = device.get("NAME") or device.get("ID_MODEL") or ""
        devpath = device.get("DEVPATH")  # unique identifier

        # ✅ prevent multiple triggers for same USB
        if TARGET_DEVICE.lower() in name.lower() and devpath not in triggered_devices:
            triggered_devices.add(devpath)

            print(f"[SIMULATOR] Target detected: {name}")

            time.sleep(1)  # allow system to stabilize
            simulate()


if __name__ == "__main__":
    monitor_and_trigger()
