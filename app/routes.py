from app import app
from flask import abort, redirect, url_for, render_template, Flask, request, flash, make_response, session, send_file, send_from_directory, Response
from os import path
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from .lib import prepare_test1
from .lib import prepare_test2
from .lib import prepare_test3
from .lib import prepare_test4
from .lib import processing
from .lib import plotter
from .lib import read_results_test1
from .lib import read_results_test2
from .lib import read_results_test3
from .lib import read_results_test4
from .lib import vreg_calculator_old
from .lib import vreg_calculator
from .lib.kepler import comp_solver




# folder = 'C:\Temp\dorsum'
folder = '/Users/nickas/Documents/_to_upload/dorsum'
#folder = r'\\akl-file-02\Share\Harshad\dorsum_test'
#folder = ""
card1 = ""
card2 = ""
frequency = ""
freq = ""
result_test3_full = pd.DataFrame()
result_fvt = pd.DataFrame()
result_fvt_single = pd.DataFrame()
result_fvt_single_3 = pd.DataFrame()

cards11 = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True}
cards12 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}
cards21 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
cards22 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}

set_points = {0:'Pluto+', 1:'AKM2156'}

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
        folder = request.form.get('folder')

    message_success, message_text, file, time, result = read_results_test1.read(folder)
    print(message_text)

    if not message_success:
        result = pd.DataFrame()


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
        folder = request.form.get('folder')

    message_success, message_text, file, freq, time, result = read_results_test2.read(folder)
    print(message_text)

    if message_success:
        vregs_table = vreg_calculator.calculate(result)
    else:
        vregs_table = pd.DataFrame()
        result = pd.DataFrame()


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
    entered_set_point = ""
    card11_available = []
    card12_available = []




    if request.method == 'GET' and request.args.get('folder'):
        folder = request.args.get('folder')
        #print(folder)


    message_success, message_text, file, freq, time, result = read_results_test2.read(folder)
    print(message_text)

    if message_success:
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

        #folder = request.form.get('folder')
        entered_set_point = request.form.get('setpoint')
        # frequency = request.form.get('freq')
        #
        message_success, message_text, file, freq, time, result = read_results_test2.read(folder)
        print(message_text)

        duts_number = len(card_total)
        if duts_number < 1:
            message_text = message_text + " *** Number of DUTs can't be 0!"
            message_success = False
        else:
            duts_number_string = str(duts_number)

        if message_success:
            vregs_table = vreg_calculator.calculate(result)
            success, message, config_file, script_file = prepare_test3.prepare(folder, card1, card2, freq, vregs_table, entered_set_point)
            if success:
                message_text = " Now you can start Test-3"
            else:
                message_success = False
                message_text = message
        else:
            card11_available = []
            card12_available = []
            file = ""
            entered_card1 = ""
            entered_card2 = ""
            duts_number_string = ""
            cards11 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False,
                       11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
            cards12 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False,
                       25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}
            cards21 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False,
                       10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
            cards22 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False,
                       25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}


    else:
        card11 = card11_available
        card12 = card12_available
        cards11 = processing.update_card(cards11, card11)
        cards12 = processing.update_card(cards12, card12)



    return render_template('test3.html',
                           folder = folder,
                           entered_folder=folder,
                           set_points=set_points,
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
                           input_file=file,
                           freq = freq,
                           entered_frequency=freq,
                           entered_set_point=entered_set_point,
                           duts_number=duts_number_string)



@app.route('/chu/test3/result', methods=['post', 'get'])
def test3_result():
    global folder
    global card1
    global card2
    global frequency
    global freq
    global vreg
    global vreg_threshold
    global ppm
    global ppm_threshold
    global result_test3_full
    global result_fvt_single_3

    interpol = 1

    result_fvt_single_3 = pd.DataFrame()

    if request.method == 'GET' and request.args.get('pos') and request.args.get('pos') != 'ALL':
        entered_pos = int(request.args.get('pos'))
    else:
        entered_pos = 'ALL'

    if request.method == 'POST':
        folder = request.form.get('folder')
        if request.form.get('inter'):
            interpol = int(request.form.get('inter'))
            if interpol < 1:
                interpol = 1

    message_success, message_text, file, freq, time, bad_units, result_test3_full, result_cutted = read_results_test3.read(folder, interpol)
    print(message_text)

    if message_success:
        poses = result_test3_full['pos'].unique().tolist()
        poses.insert(0, 'ALL')
        if entered_pos == 'ALL':
            result_fvt_single_3 = result_test3_full
        else:
            result_fvt_single_3 = result_test3_full[result_test3_full['pos'] == entered_pos]

    else:
        poses = []

    try:
        solver_output = comp_solver.solve(result_cutted)
        print(solver_output)
        print(solver_output.info())
    except:
        message_text = message_text + " *** Problem with solver calculations"
        message_success = False

    vregs_table = pd.DataFrame()

    # print(len(bad_units))

    if len(bad_units) > 1:
        bad_units_exist = True
    else:
        bad_units_exist = False


    return render_template('test3_results.html',
                           folder=folder,
                           card1=card1,
                           card2=card2,
                           column_names=result_fvt_single_3.columns.values,
                           row_data=list(result_fvt_single_3.values.tolist()),
                           column_names_1=vregs_table.columns.values,
                           row_data_1=list(vregs_table.values.tolist()),
                           zip=zip,
                           entered_folder=folder,
                           message_success=message_success,
                           message_text=message_text,
                           file=file,
                           time=time,
                           freq=freq,
                           bad_units=bad_units,
                           bad_units_exist=bad_units_exist,
                           entered_interpol=interpol,
                           poses=poses,
                           entered_pos=entered_pos,
                           frequency=frequency)



@app.route('/chu/test3/result/plot.png', methods=['post', 'get'])
def test3_plot_png():
    global result_test3_full
    global result_fvt_single_3
    global freq


    title = "Test-3 results (frequency = " + str(freq) + "MHz)"
    fig = plotter.plot(result_fvt_single_3, title)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')



@app.route('/chu/test4', methods=['post', 'get'])
def test4():
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
    entered_set_point = ""
    card11_available = []
    card12_available = []
    interpol = 1




    if request.method == 'GET' and request.args.get('folder'):
        folder = request.args.get('folder')
        #print(folder)

    message_success, message_text, file, freq, time, bad_units, result_test3_full, result_cutted = read_results_test3.read(
        folder, interpol)
    print(message_text)

    if message_success:
        card11_available = result_cutted[result_cutted['pos'] < 17]['pos'].unique().tolist()
        card12_available = result_cutted[result_cutted['pos'] > 16]['pos'].unique().tolist()

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

        #folder = request.form.get('folder')
        entered_set_point = request.form.get('setpoint')
        # frequency = request.form.get('freq')
        #
        message_success, message_text, file, freq, time, bad_units, result_test3_full, result_cutted = read_results_test3.read(
            folder, interpol)
        print(message_text)

        duts_number = len(card_total)
        if duts_number < 1:
            message_text = message_text + " *** Number of DUTs can't be 0!"
            message_success = False
        else:
            duts_number_string = str(duts_number)

        if message_success:
            pass
            #!!!!!!add solver here
            #vregs_table = vreg_calculator.calculate(result_cutted)
            #success, message, config_file, script_file = prepare_test4.prepare(folder, card1, card2, freq, vregs_table, entered_set_point)
            # if success:
            #     message_text = " Now you can start Test-3"
            # else:
            #     message_success = False
            #     message_text = message
        else:
            card11_available = []
            card12_available = []
            file = ""
            entered_card1 = ""
            entered_card2 = ""
            duts_number_string = ""
            cards11 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False,
                       11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
            cards12 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False,
                       25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}
            cards21 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False,
                       10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
            cards22 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False,
                       25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}


    else:
        card11 = card11_available
        card12 = card12_available
        cards11 = processing.update_card(cards11, card11)
        cards12 = processing.update_card(cards12, card12)



    return render_template('test4.html',
                           folder = folder,
                           entered_folder=folder,
                           set_points=set_points,
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
                           input_file=file,
                           freq = freq,
                           entered_frequency=freq,
                           entered_set_point=entered_set_point,
                           duts_number=duts_number_string)


@app.route('/chu/test4/result', methods=['post', 'get'])
def test4_result():
    global folder
    global card1
    global card2
    global frequency
    global vreg
    global vreg_threshold
    global ppm
    global ppm_threshold
    global result_fvt
    global result_fvt_single

    interpol = 1
    result_fvt_single = pd.DataFrame()

    if request.method == 'GET' and request.args.get('pos') and request.args.get('pos') != 'ALL':
        entered_pos = int(request.args.get('pos'))
    else:
        entered_pos = 'ALL'

    if request.method == 'POST':
        folder = request.form.get('folder')
        if request.form.get('inter'):
            interpol = int(request.form.get('inter'))
            if interpol < 1:
                interpol = 1

    message_success, message_text, file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, interpol)
    print(message_text)

    if message_success:
        poses = result_fvt['pos'].unique().tolist()
        poses.insert(0, 'ALL')
        if entered_pos == 'ALL':
            result_fvt_single = result_fvt
        else:
            result_fvt_single = result_fvt[result_fvt['pos'] == entered_pos]

    else:
        poses = []

    # try:
    #     solver_output = comp_solver.solve(result_cutted)
    #     print(solver_output)
    #     print(solver_output.info())
    # except:
    #     message_text = message_text + " *** Problem with solver calculations"
    #     message_success = False

    vregs_table = pd.DataFrame()

    if len(bad_units) > 1:
        bad_units_exist = True
    else:
        bad_units_exist = False

    print("entered_pos = " + str(entered_pos))


    return render_template('test4_results.html',
                           folder=folder,
                           card1=card1,
                           card2=card2,
                           column_names=result_fvt_single.columns.values,
                           row_data=list(result_fvt_single.values.tolist()),
                           column_names_1=result_calculated.columns.values,
                           row_data_1=list(result_calculated.values.tolist()),
                           zip=zip,
                           entered_folder=folder,
                           message_success=message_success,
                           message_text=message_text,
                           file=file,
                           time=time,
                           freq=freq,
                           bad_units=bad_units,
                           bad_units_exist=bad_units_exist,
                           entered_interpol=interpol,
                           poses=poses,
                           entered_pos=entered_pos,
                           frequency=frequency)


@app.route('/chu/test4/result/plot.png', methods=['post', 'get'])
def test4_plot_png():
    global result_fvt
    global result_fvt_single


    title = "Test-4 results"
    fig = plotter.plot(result_fvt_single, title)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')