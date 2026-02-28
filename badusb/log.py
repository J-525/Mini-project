import os
import time
import hashlib
import config

shell=os.environ.get("SHELL")
history=f"~/.{shell[9:]}_history"
print(history)
HISTORY_FILE = os.path.expanduser(history)
print(HISTORY_FILE)
SUSPICIOUS_COMMANDS = [
    "wget", "curl", "nc", "netcat",
    "bash -i", "chmod 777",
    "/dev/tcp", "mkfs", "dd",
    "rm -rf", "sudo su"
]

def hash_file(filepath):
    """Generate hash of file"""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def check_suspicious_command(command):
    """Check if command contains suspicious keyword"""
    for keyword in SUSPICIOUS_COMMANDS:
        if keyword in command:
            return True
    return False

def monitor_history():
    print(" Monitoring Shell History...")
    
    if not os.path.exists(HISTORY_FILE):
        print("No bash history found.")
        return
    
    last_hash = hash_file(HISTORY_FILE)

    while True:
        time.sleep(5)

        current_hash = hash_file(HISTORY_FILE)

        if current_hash != last_hash:
            print("\n⚠ New Command Detected!")
            
            with open(HISTORY_FILE, "r") as f:
                lines = f.readlines()
                last_command = lines[-1].strip()
                print("Command:", last_command)

                if check_suspicious_command(last_command):
                    print(" ALERT: Suspicious Command Detected!")
                else:
                    print(" Command looks normal.")

            last_hash = current_hash

if __name__ == "__main__":
    monitor_history()