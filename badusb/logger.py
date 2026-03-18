import logging

logging.basicConfig(
    filename="badusb.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_alert(message):
    logging.info(message)