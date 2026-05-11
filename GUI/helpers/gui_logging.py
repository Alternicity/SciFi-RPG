#GUI.helpers.gui_logging.py
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "gui_logs.txt"
)


def gui_log(message):

    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
