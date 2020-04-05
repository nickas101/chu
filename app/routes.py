from app import app
from flask import abort, redirect, url_for, render_template, Flask, request, flash, make_response, session, send_file, send_from_directory, Response
from os import path

from .lib import prepare_test1




#folder = 'C:\Temp\dorsum'
folder = r'\\akl-file-02\Share\Harshad\dorsum_test'
#folder = ""
card1 = ""
card2 = ""
frequency = ""
cards1 = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
cards2 = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']


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
    global frequency

    config_file = ""
    script_file = ""
    duts_number_string = ""
    message_success = False
    message_text = ""


    if request.method == 'POST':

        message_success = True

        folder = request.form.get('folder')
        card1 = request.form.get('card1')
        card2 = request.form.get('card2')
        frequency = request.form.get('freq')

        print("Folder = " + str(folder))
        print("Card-1 = " + str(card1))
        print("Card-2 = " + str(card2))
        print("Frequency = " + str(frequency))

        duts_number = int(card1) + int(card2)
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
                           cards1=cards1,
                           cards2=cards2,
                           entered_folder=folder,
                           entered_card1=card1,
                           entered_card2=card2,
                           entered_frequency=frequency,
                           message_success=message_success,
                           message_text=message_text,
                           config_file=config_file,
                           script_file=script_file,
                           duts_number=duts_number_string
                           )


@app.route('/chu/test2', methods=['post', 'get'])
def test2():
    global folder
    global card1
    global card2
    global frequency


    return render_template('test2.html', folder = folder, card1 = card1, card2 = card2, frequency = frequency)


@app.route('/chu/test3', methods=['post', 'get'])
def test3():
    global folder
    global card1
    global card2
    global frequency


    return render_template('test3.html', folder = folder, card1 = card1, card2 = card2, frequency = frequency)


@app.route('/chu/test4', methods=['post', 'get'])
def test4():
    global folder
    global card1
    global card2
    global frequency


    return render_template('test3.html', folder = folder, card1 = card1, card2 = card2, frequency = frequency)