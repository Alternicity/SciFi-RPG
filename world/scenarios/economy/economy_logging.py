#world.scenarios.economy.economy_logging.py

import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "economy",
    "economy_log.txt"
)

def economy_log(message):

    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")