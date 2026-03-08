import os
import time

shell=os.environ.get("SHELL")
shell_name = os.path.basename(shell)
history_file = os.path.expanduser(f"~/.{shell_name}_history")

#print("test")

SUSPICIOUS_COMMANDS = [
    "wget", "curl", "nc", "netcat",
    f"{shell_name} -i", "chmod 777",
    "/dev/tcp", "mkfs", "dd",
    "rm -rf", "sudo su" ,"sudo"
]
def sus_finder():

    if not os.path.exists(history_file):
        print(f"History file not found: {history_file}")
        return ""

    with open(history_file, "r", errors="ignore") as f:
        lines = f.readlines()
    
    sus=lines[-5:]

    return ''.join(sus)
    


def beep(risk):
    sus=sus_finder()
    #zprint(sus)
    print("\nALERT: BadUSB attack detected!")
    print(f"Risk Level: {risk}")
    for command in SUSPICIOUS_COMMANDS:
        if command in sus:
            print(f"\n ALERT: Suspicious command detected: {command}")
            #print(f"Context: {sus}")
            print("Time:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            break


#if __name__ == "__main__":
#    beep(10)