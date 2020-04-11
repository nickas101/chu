from app import app
from flask import abort, redirect, url_for, render_template, Flask, request, flash, make_response, session, send_file, send_from_directory, Response
from os import path

from .lib import prepare_test1
from .lib import prepare_test2
from .lib import processing
from .lib import read_results_test1
from .lib import read_results_test2
from .lib import vreg_calculator_old
from .lib import vreg_calculator




# folder = 'C:\Temp\dorsum'
folder = '/Users/nickas/Documents/_to_upload/dorsum'
#folder = r'\\akl-file-02\Share\Harshad\dorsum_test'
#folder = ""
card1 = ""
card2 = ""
frequency = ""
#cards1 = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
#cards2 = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']

# cards11 = {'01': True, '02': True, '03': True, '04': True, '05': True, '06': True, '07': True, '08': True, '09': True, '10': True, '11': True, '12': True, '13': True, '14': True, '15': True, '16': True}
# cards12 = {'17': False, '18': False, '19': False, '20': False, '21': False, '22': False, '23': False, '24': False, '25': False, '26': False, '27': False, '28': False, '29': False, '30': False, '31': False, '32': False}
# cards21 = {'01': False, '02': False, '03': False, '04': False, '05': False, '06': False, '07': False, '08': False, '09': False, '10': False, '11': False, '12': False, '13': False, '14': False, '15': False, '16': False}
# cards22 = {'17': False, '18': False, '19': False, '20': False, '21': False, '22': False, '23': False, '24': False, '25': False, '26': False, '27': False, '28': False, '29': False, '30': False, '31': False, '32': False}

cards11 = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True}
cards12 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}
cards21 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
cards22 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}


vreg = 1.9
vreg_threshold = 0.2
ppm = 0
ppm_threshold = 0.5



@app.route('/')
def index():
    return redirect(url_for('test1'))


@app.route('/chu', methods=['post', 'get'])
def chu():
    return redirect(url_for('test1'))


@app.route('/chu/test1', methods=['post', 'get'])
def test1():
    global folder
    global card1
    global card2
    global cards11
    global cards12
    global cards21
    global cards22
    global frequency

    config_file = ""
    script_file = ""
    duts_number_string = ""
    message_success = True
    message_text = ""
    entered_card1 = ""
    entered_card2 = ""


    if request.method == 'POST':

        card11 = request.form.getlist('card11')
        card12 = request.form.getlist('card12')
        card1 = card11 + card12

        card21 = request.form.getlist('card21')
        card22 = request.form.getlist('card22')
        card2 = card21 + card22

        card_total = card1 + card2

        cards11 = processing.update_card(cards11, card11)
        cards12 = processing.update_card(cards12, card12)
        cards21 = processing.update_card(cards21, card21)
        cards22 = processing.update_card(cards22, card22)

        entered_card1 = processing.join_entered_cards(card11, card12)
        entered_card2 = processing.join_entered_cards(card21, card22)

        folder = request.form.get('folder')
        frequency = request.form.get('freq')

        print("Folder = " + str(folder))
        print("Card-1 = " + str(card1))
        print("Card-2 = " + str(card2))
        print("Frequency = " + str(frequency))

        duts_number = len(card_total)
        if duts_number < 1:
            message_text = message_text + " *** Number of DUTs can't be 0!"
            message_success = False
        else:
            duts_number_string = str(duts_number)

        try:
            float(frequency)
        except:
            message_text = message_text + " *** Wrong frequency!"
            frequency = ""
            message_success = False

        if not path.os.path.isdir(folder):
            message_text = message_text + " *** Wrong folder!"
            folder = ""
            message_success = False


        if message_success:
            success, message, config_file, script_file = prepare_test1.prepare(folder, card1, card2, frequency)
            if success:
                message_text = " Now you can start Test-1"
            else:
                message_success = False
                message_text = message


    return render_template('test1.html',
                           cards11=cards11,
                           cards12=cards12,
                           cards21=cards21,
                           cards22=cards22,
                           entered_folder=folder,
                           entered_card1=entered_card1,
                           entered_card2=entered_card2,
                           entered_frequency=frequency,
                           message_success=message_success,
                           message_text=message_text,
                           config_file=config_file,
                           script_file=script_file,
                           duts_number=duts_number_string
                           )


@app.route('/chu/test1/result', methods=['post', 'get'])
def test1_result():
    global folder
    global card1
    global card2
    global frequency
    global vreg
    global vreg_threshold
    global ppm
    global ppm_threshold


    if request.method == 'POST':
        vreg_threshold = float(request.form.get('vreg_threshold'))
        ppm_threshold = float(request.form.get('ppm_threshold'))

    message_success, message_text, file, time, result = read_results_test1.read(folder)


    return render_template('test1_results.html',
                           folder=folder,
                           card1=card1,
                           card2=card2,
                           column_names=result.columns.values,
                           row_data=list(result.values.tolist()),
                           zip=zip,
                           entered_folder=folder,
                           message_success=message_success,
                           message_text=message_text,
                           file=file,
                           time=time,
                           vreg=vreg,
                           vreg_threshold=vreg_threshold,
                           ppm=ppm,
                           ppm_threshold=ppm_threshold,
                           frequency=frequency)


@app.route('/chu/test2', methods=['post', 'get'])
def test2():
    global folder
    global card1
    global card2
    global cards11
    global cards12
    global cards21
    global cards22
    global frequency

    config_file = ""
    script_file = ""
    duts_number_string = ""
    message_success = True
    message_text = ""
    entered_card1 = ""
    entered_card2 = ""


    if request.method == 'POST':

        card11 = request.form.getlist('card11')
        card12 = request.form.getlist('card12')
        card1 = card11 + card12

        card21 = request.form.getlist('card21')
        card22 = request.form.getlist('card22')
        card2 = card21 + card22

        card_total = card1 + card2

        cards11 = processing.update_card(cards11, card11)
        cards12 = processing.update_card(cards12, card12)
        cards21 = processing.update_card(cards21, card21)
        cards22 = processing.update_card(cards22, card22)
        #
        # print("card11")
        # print(card11)
        # print("cards11")
        # print(cards11)

        entered_card1 = processing.join_entered_cards(card11, card12)
        entered_card2 = processing.join_entered_cards(card21, card22)

        folder = request.form.get('folder')
        frequency = request.form.get('freq')

        print("Folder = " + str(folder))
        print("Card-1 = " + str(card1))
        print("Card-2 = " + str(card2))
        print("Frequency = " + str(frequency))

        duts_number = len(card_total)
        if duts_number < 1:
            message_text = message_text + " *** Number of DUTs can't be 0!"
            message_success = False
        else:
            duts_number_string = str(duts_number)

        try:
            float(frequency)
        except:
            message_text = message_text + " *** Wrong frequency!"
            frequency = ""
            message_success = False

        if not path.os.path.isdir(folder):
            message_text = message_text + " *** Wrong folder!"
            folder = ""
            message_success = False


        if message_success:
            success, message, config_file, script_file = prepare_test2.prepare(folder, card1, card2, frequency)
            if success:
                message_text = " Now you can start Test-2"
            else:
                message_success = False
                message_text = message


    return render_template('test2.html',
                           cards11=cards11,
                           cards12=cards12,
                           cards21=cards21,
                           cards22=cards22,
                           entered_folder=folder,
                           entered_card1=entered_card1,
                           entered_card2=entered_card2,
                           entered_frequency=frequency,
                           message_success=message_success,
                           message_text=message_text,
                           config_file=config_file,
                           script_file=script_file,
                           duts_number=duts_number_string
                           )


@app.route('/chu/test2/result', methods=['post', 'get'])
def test2_result():
    global folder
    global card1
    global card2
    global frequency
    global vreg
    global vreg_threshold
    global ppm
    global ppm_threshold


    if request.method == 'POST':
        pass
        # vreg_threshold = float(request.form.get('vreg_threshold'))
        # ppm_threshold = float(request.form.get('ppm_threshold'))

    message_success, message_text, file, freq, time, result = read_results_test2.read(folder)
    vregs_table = vreg_calculator.calculate(result)

    #print(vregs_table)


    return render_template('test2_results.html',
                           folder=folder,
                           card1=card1,
                           card2=card2,
                           column_names=result.columns.values,
                           row_data=list(result.values.tolist()),
                           column_names_1=vregs_table.columns.values,
                           row_data_1=list(vregs_table.values.tolist()),
                           zip=zip,
                           entered_folder=folder,
                           message_success=message_success,
                           message_text=message_text,
                           file=file,
                           time=time,
                           freq=freq,
                           frequency=frequency)


@app.route('/chu/test3', methods=['post', 'get'])
def test3():
    global folder
    global card1
    global card2
    global cards11
    global cards12
    global cards21
    global cards22
    global frequency

    config_file = ""
    script_file = ""
    duts_number_string = ""
    message_success = True
    message_text = ""
    entered_card1 = ""
    entered_card2 = ""


    message_success, message_text, file, freq, time, result = read_results_test2.read(folder)

    card11_available = result[result['pos'] < 17]['pos'].unique().tolist()
    card12_available = result[result['pos'] > 16]['pos'].unique().tolist()

    if request.method == 'POST':

        card11 = request.form.getlist('card11')
        card12 = request.form.getlist('card12')
        card1 = card11 + card12

        card21 = request.form.getlist('card21')
        card22 = request.form.getlist('card22')
        card2 = card21 + card22

        card_total = card1 + card2

        cards11 = processing.update_card(cards11, card11)
        cards12 = processing.update_card(cards12, card12)
        cards21 = processing.update_card(cards21, card21)
        cards22 = processing.update_card(cards22, card22)

        entered_card1 = processing.join_entered_cards(card11, card12)
        entered_card2 = processing.join_entered_cards(card21, card22)

        folder = request.form.get('folder')
        # frequency = request.form.get('freq')
        #
        # print("Folder = " + str(folder))
        # print("Card-1 = " + str(card1))
        # print("Card-2 = " + str(card2))
        # print("Frequency = " + str(frequency))

        duts_number = len(card_total)
        if duts_number < 1:
            message_text = message_text + " *** Number of DUTs can't be 0!"
            message_success = False
        else:
            duts_number_string = str(duts_number)
    else:
        card11 = card11_available
        card12 = card12_available
        cards11 = processing.update_card(cards11, card11)
        cards12 = processing.update_card(cards12, card12)



    return render_template('test3.html',
                           folder = folder,
                           entered_folder=folder,
                           card1 = card1,
                           card2 = card2,
                           card11_available=card11_available,
                           card12_available=card12_available,
                           cards11=cards11,
                           cards12=cards12,
                           cards21=cards21,
                           cards22=cards22,
                           entered_card1=entered_card1,
                           entered_card2=entered_card2,
                           message_success=message_success,
                           message_text=message_text,
                           config_file=config_file,
                           script_file=script_file,
                           freq = freq,
                           entered_frequency=freq,
                           duts_number=duts_number_string)


@app.route('/chu/test4', methods=['post', 'get'])
def test4():
    global folder
    global card1
    global card2
    global frequency


    return render_template('test3.html', folder = folder, card1 = card1, card2 = card2, frequency = frequency)