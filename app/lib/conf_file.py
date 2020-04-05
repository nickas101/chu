import os
from datetime import datetime



config_file = "chamber-U config.hwc"

def create_config(folder):

    config_file_name = config_file.replace(".hwc", "")

    current_time = datetime.now()
    file_time = str(current_time)
    file_time = file_time.replace(" ", "_")
    file_time = file_time.replace(":", "-")
    file_time = file_time.split(".")
    try:
        os.rename(folder + '/' + config_file, folder + '/' + config_file_name + '_' + str(file_time[0]) + '.hwc')
    except:
        pass

    with open('app/scripts/Chamber-U Config.hwc', 'r') as file:
        #data = file.read().replace('\n', '')
        data = file.read()

    with open(folder + '/' + config_file, 'w') as output_file:
        output_file.write(data)


    return config_file