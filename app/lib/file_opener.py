from pathlib import Path
from os import path
from datetime import datetime


def open_file(folder, test_results_file):

    message_text = ""
    message_success = True
    time = ""
    lines = ""

    data_folder = Path(folder)
    full_path = data_folder / test_results_file

    if not path.isfile(full_path):
        message_text = message_text + " *** Input file not found!"
        message_success = False
    else:
        time_raw = path.getmtime(full_path)
        time_string = str(datetime.fromtimestamp(time_raw))
        time = time_string.split('.')[0]

        with open(full_path, 'r') as file:
            lines = file.readlines()

    return message_success, message_text, time, lines