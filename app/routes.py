from app import app
from flask import abort, redirect, url_for, render_template, Flask, request, flash, make_response, session, send_file, send_from_directory, Response
from os import path
from pathlib import Path
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from .lib import prepare_test1
from .lib import prepare_test2
from .lib import prepare_test3
from .lib import prepare_test4
from .lib import card_processing
from .lib import plotter_test3
from .lib import plotter_test4
from .lib import read_results_test1
from .lib import read_results_test2
from .lib import read_results_test3
from .lib import read_results_test4
from .lib import vreg_calculator
from .lib import solver_table_converter
from .lib.kepler import comp_solver
from .lib import solver_wrapper




#folder = 'C:\Temp\dorsum'
folder = '/Users/nickas/Documents/_to_upload/dorsum'
# folder = r'\\akl-file-02\Share\Harshad\dorsum_test'
#folder = ""

temporary_plot_file = 'plot.png'
temporary_folder_local = 'app/temp_files/'
temporary_plot_folder = Path.cwd() / temporary_folder_local
templates_folder_local = 'app/templates'
templates_folder = Path.cwd() / templates_folder_local
card1 = ""
card2 = ""
frequency = ""
freq = ""
result_test3_full = pd.DataFrame()
result_fvt = pd.DataFrame()
result_fvt_single = pd.DataFrame()
result_fvt_single_3 = pd.DataFrame()
result_fvt_single_4_3 = pd.DataFrame()
prediction = pd.DataFrame()

cards11 = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True}
cards12 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}
cards21 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
cards22 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}

set_points = {0:'Pluto+', 1:'AKM2156'}

vreg = 1.9
vreg_threshold = 0.2
ppm = 0
ppm_threshold = 0.5
temp_min = -40
temp_max = 95
step = 1
temp_min_previous = -40
temp_max_previous = 95
step_previous = 1
interpol = 1
high_temp_limit = 95
solver_cut_number = 7


@app.route('/')
def index():
    return redirect(url_for('test1'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(templates_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


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

        cards11 = card_processing.update_card(cards11, card11)
        cards12 = card_processing.update_card(cards12, card12)
        cards21 = card_processing.update_card(cards21, card21)
        cards22 = card_processing.update_card(cards22, card22)

        entered_card1 = card_processing.join_entered_cards(card11, card12)
        entered_card2 = card_processing.join_entered_cards(card21, card22)

        if request.form.get('folder'):
            folder = request.form.get('folder')
        else:
            folder = ''

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

        if not path.isdir(folder):
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

        cards11 = card_processing.update_card(cards11, card11)
        cards12 = card_processing.update_card(cards12, card12)
        cards21 = card_processing.update_card(cards21, card21)
        cards22 = card_processing.update_card(cards22, card22)

        entered_card1 = card_processing.join_entered_cards(card11, card12)
        entered_card2 = card_processing.join_entered_cards(card21, card22)

        if request.form.get('folder'):
            folder = request.form.get('folder')
        else:
            folder = ''

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

        if not path.isdir(folder):
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
    entered_card1 = ""
    entered_card2 = ""
    entered_set_point = ""
    card11_available = []
    card12_available = []

    if request.method == 'GET' and request.args.get('folder'):
        folder = request.args.get('folder')

    message_success, message_text, file, freq, time, result = read_results_test2.read(folder)
    print(message_text)

    if message_success:
        card11_available = result[result['pos'] < 17]['pos'].unique().tolist()
        card12_available = result[result['pos'] > 16]['pos'].unique().tolist()

    if request.method == 'POST':

        print('folder = ' + str(folder))

        card11 = request.form.getlist('card11')
        card12 = request.form.getlist('card12')
        card1 = card11 + card12

        card21 = request.form.getlist('card21')
        card22 = request.form.getlist('card22')
        card2 = card21 + card22

        card_total = card1 + card2

        cards11 = card_processing.update_card(cards11, card11)
        cards12 = card_processing.update_card(cards12, card12)
        cards21 = card_processing.update_card(cards21, card21)
        cards22 = card_processing.update_card(cards22, card22)

        entered_card1 = card_processing.join_entered_cards(card11, card12)
        entered_card2 = card_processing.join_entered_cards(card21, card22)

        entered_set_point = request.form.get('setpoint')

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
        cards11 = card_processing.update_card(cards11, card11)
        cards12 = card_processing.update_card(cards12, card12)

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
    global interpol
    global high_temp_limit
    global prediction

    result_fvt_single_3 = pd.DataFrame()
    solver_output = pd.DataFrame()
    solver_output_short = pd.DataFrame()
    entered_pos = 'ALL'
    bad_units_solver = ''

    if request.method == 'GET':
        if request.args.get('pos') and request.args.get('pos') != 'ALL':
            entered_pos = int(request.args.get('pos'))

        if request.args.get('high_temp_limit'):
            try:
                high_temp_limit = int(request.args.get('high_temp_limit'))
            except:
                pass

    if request.method == 'POST':
        folder = request.form.get('folder')
        if request.form.get('inter'):
            interpol = int(request.form.get('inter'))
            if interpol < 1:
                interpol = 1

    message_success, message_text, file, freq, time, bad_units, result_test3_full, result_cutted, vreg_table_from_test3 = read_results_test3.read(folder, interpol)

    if message_success:
        poses = result_test3_full['pos'].unique().tolist()
        poses.insert(0, 'ALL')
        if entered_pos == 'ALL':
            result_fvt_single_3 = result_test3_full[result_test3_full['Temp'] < high_temp_limit]
        else:
            result_fvt_single_3 = result_test3_full[
                (result_test3_full['pos'] == entered_pos) & (result_test3_full['Temp'] < high_temp_limit)]

        success_solver, message_solver, solver_output, solver_output_short, prediction, bad_units_solver, bad_units_list_solver = solver_wrapper.wrap(result_cutted, solver_cut_number)
        if not success_solver:
            message_text = message_text + message_solver
            message_success = False

    else:
        poses = []

    if len(bad_units) > 1 and len(bad_units_solver) > 1:
        bad_units = bad_units + ', ' + bad_units_solver
    elif len(bad_units_solver) > 1:
        bad_units = bad_units_solver

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
                           column_names_1=solver_output_short.columns.values,
                           row_data_1=list(solver_output_short.values.tolist()),
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
                           entered_high_temp_limit=high_temp_limit,
                           frequency=frequency)


@app.route('/chu/test3/result/plot.png', methods=['post', 'get'])
def test3_plot_png():
    global result_test3_full
    global result_fvt_single_3
    global freq
    global prediction

    title = "Test-3 results (frequency = " + str(freq) + "MHz)"
    fig = plotter_test3.plot(result_fvt_single_3, prediction, title)

    fig.savefig(Path(temporary_folder_local) / temporary_plot_file, bbox_inches='tight')

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
    global temp_max
    global temp_min
    global step
    global temp_min_previous
    global temp_max_previous
    global step_previous

    config_file = ""
    script_file = ""
    duts_number_string = ""
    message_success = True
    message_text = ""
    entered_card1 = ""
    entered_card2 = ""
    card11_available = []
    card12_available = []
    interpol = 1
    temp_range = ""
    solver_table = pd.DataFrame()

    if request.method == 'GET' and request.args.get('folder'):
        folder = request.args.get('folder')

    success_test3, message_test3, file, freq, time, bad_units, result_test3_full, result_cutted3, vreg_table_from_test3 = read_results_test3.read(
        folder, interpol)

    if success_test3:
        success_solver, message_solver, solver_output, solver_output_short, prediction, bad_units_solver, bad_units_list_solver = solver_wrapper.wrap(result_cutted3, solver_cut_number)
        if success_solver:
            result_cutted = result_cutted3[~result_cutted3['pos'].isin(bad_units_list_solver)]

        else:
            result_cutted = result_cutted3
            message_text = message_text + message_solver
            message_success = False

        card11_available = result_cutted[result_cutted['pos'] < 17]['pos'].unique().tolist()
        card12_available = result_cutted[result_cutted['pos'] > 16]['pos'].unique().tolist()
    else:
        message_text = message_text + message_test3
        message_success = False

    if request.method == 'POST':
        card11 = request.form.getlist('card11')
        card12 = request.form.getlist('card12')
        card1 = card11 + card12

        card21 = request.form.getlist('card21')
        card22 = request.form.getlist('card22')
        card2 = card21 + card22

        card_total = card1 + card2

        cards11 = card_processing.update_card(cards11, card11)
        cards12 = card_processing.update_card(cards12, card12)
        cards21 = card_processing.update_card(cards21, card21)
        cards22 = card_processing.update_card(cards22, card22)

        entered_card1 = card_processing.join_entered_cards(card11, card12)
        entered_card2 = card_processing.join_entered_cards(card21, card22)

        temp_max = request.form.get('temp_max')
        temp_min = request.form.get('temp_min')
        step = request.form.get('step')

        try:
            if int(temp_max) < int(temp_min):
                temp_temp = temp_max
                temp_max = temp_min
                temp_min = temp_temp
            if int(step) < 1:
                step = 1
            temp_range = str(int(temp_max)) + ' ' + str(int(temp_min)) + ' ' + str(int(step))
            temp_min_previous = temp_min
            temp_max_previous = temp_max
            step_previous = step

        except:
            message_text = message_text + " *** Temperature range is incorrect!"
            message_success = False
            temp_max = temp_max_previous
            temp_min = temp_min_previous
            step = step_previous

        success_test3, message_test3, file, freq, time, bad_units, result_test3_full, result_cutted, vreg_table_from_test3 = read_results_test3.read(
            folder, interpol)

        duts_number = len(card_total)
        if duts_number < 1:
            message_text = message_text + " *** Number of DUTs can't be 0!"
            message_success = False
        else:
            duts_number_string = str(duts_number)

        if success_test3 and message_success:
            success, message, config_file, script_file = prepare_test4.prepare(folder, card1, card2, freq, solver_output, vreg_table_from_test3, temp_range)
            if success:
                message_text = " Now you can start Test-4"
            else:
                message_success = False
                message_text = message_text + message_test3
        else:
            # card11_available = []
            # card12_available = []
            file = ""
            entered_card1 = ""
            entered_card2 = ""
            duts_number_string = ""
            # cards11 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False,
            #            11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
            # cards12 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False,
            #            25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}
            # cards21 = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False,
            #            10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False}
            # cards22 = {17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False,
            #            25: False, 26: False, 27: False, 28: False, 29: False, 30: False, 31: False, 32: False}

    else:
        card11 = card11_available
        card12 = card12_available
        cards11 = card_processing.update_card(cards11, card11)
        cards12 = card_processing.update_card(cards12, card12)

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
                           freq=freq,
                           entered_frequency=freq,
                           entered_temp_min=temp_min,
                           entered_temp_max=temp_max,
                           entered_step=step,
                           duts_number=duts_number_string)


@app.route('/chu/test4/result', methods=['post', 'get'])
def test4_result():
    global folder
    global card1
    global card2
    global frequency
    global freq
    global vreg
    global vreg_threshold
    global ppm
    global ppm_threshold
    global result_fvt
    global result_fvt_single
    global result_fvt_single_4_3
    global high_temp_limit

    interpol = 1
    ppb_threshold = 50
    result_fvt_single = pd.DataFrame()
    result_fvt_single_4_3 = pd.DataFrame()
    message_text = ''
    file3 = ''
    time3 = ''
    entered_pos = 'ALL'

    if request.method == 'GET':
        if request.args.get('pos') and request.args.get('pos') != 'ALL':
            entered_pos = int(request.args.get('pos'))

        if request.args.get('high_temp_limit'):
            try:
                high_temp_limit = int(request.args.get('high_temp_limit'))
            except:
                pass

    if request.method == 'POST':
        folder = request.form.get('folder')
        if request.form.get('inter'):
            interpol = int(request.form.get('inter'))
            if interpol < 1:
                interpol = 1
        if request.form.get('ppb_threshold'):
            try:
                ppb_threshold = int(request.form.get('ppb_threshold'))
            except:
                ppb_threshold = 50

    message_success, message, file4, freq, time4, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, interpol)
    print(message)

    if message_success:
        message_success, message, file3, freq, time3, bad_units3, result_test3_full, result_cutted, vreg_table_from_test3 = read_results_test3.read(
            folder, interpol)
        if message_success:
            poses = result_fvt['pos'].unique().tolist()
            poses.insert(0, 'ALL')
            if entered_pos == 'ALL':
                result_fvt_single = result_fvt
                result_fvt_single_4_3 = result_test3_full[result_test3_full['Temp'] < high_temp_limit]
            else:
                result_fvt_single = result_fvt[result_fvt['pos'] == entered_pos]
                result_fvt_single_4_3 = result_test3_full[(result_test3_full['pos'] == entered_pos) & (result_test3_full['Temp'] < high_temp_limit)]
        else:
            poses = []
            message_text = message_text + message

    else:
        poses = []
        message_text = message_text + message

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
                           file3=file3,
                           time3=time3,
                           file4=file4,
                           time4=time4,
                           freq=freq,
                           bad_units=bad_units,
                           bad_units_exist=bad_units_exist,
                           entered_interpol=interpol,
                           poses=poses,
                           entered_pos=entered_pos,
                           ppb_threshold=ppb_threshold,
                           entered_high_temp_limit=high_temp_limit,
                           frequency=frequency)


@app.route('/chu/test4/result/plot.png', methods=['post', 'get'])
def test4_plot_png():
    global result_fvt
    global result_fvt_single
    global freq
    global result_fvt_single_4_3


    title = "Test-4 results (frequency = " + str(freq) + "MHz)"
    fig = plotter_test4.plot(result_fvt_single, result_fvt_single_4_3, title)

    fig.savefig(Path(temporary_folder_local) / temporary_plot_file, bbox_inches='tight')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')


@app.route('/chu/result/plot/download', methods=['GET', 'POST'])
def download_plot():
    return send_from_directory(temporary_plot_folder, filename=temporary_plot_file, as_attachment=True)