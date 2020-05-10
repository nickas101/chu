import os
from datetime import datetime
from pathlib import Path


config_file = "chamber-U config.hwc"


def create_config(folder):
    """Create a config file from a template file."""

    current_time = datetime.now()
    file_time = str(current_time)
    file_time = file_time.replace(" ", "_")
    file_time = file_time.replace(":", "-")
    file_time = file_time.split(".")

    data_folder = Path(folder)
    file_actual = data_folder / config_file
    file_old = data_folder / config_file.replace(".hwc", '_' + str(file_time[0]) + '.hwc')

    try:
        os.rename(file_actual, file_old)
    except:
        pass

    with open('app/scripts/Chamber-U Config.hwc', 'r') as file:
        data = file.read()

    with open(file_actual, 'w') as output_file:
        output_file.write(data)

    return config_file
