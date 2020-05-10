import os
from datetime import datetime
from pathlib import Path


def rename(folder, script_file):
    """Rename an old file."""

    current_time = datetime.now()
    file_time = str(current_time)
    file_time = file_time.replace(" ", "_")
    file_time = file_time.replace(":", "-")
    file_time = file_time.split(".")

    data_folder = Path(folder)
    file_actual = data_folder / script_file
    file_old = data_folder / script_file.replace(".uscript", '_' + str(file_time[0]) + '.uscript')

    try:
        os.rename(file_actual, file_old)
        success = True
    except:
        success = False

    return success, file_actual
