import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def plot(df, title):

    fig = Figure(figsize=(16, 8))
    axis = fig.add_subplot(1, 1, 1)

    axis.set_xlabel('Temperature, degC')
    axis.set_ylabel('Frequency, ppm')

    #ax2 = axis.twinx()

    units = df['pos'].unique().tolist()

    for unit in units:
        #print(unit)
        result_single = df[df['pos'] == unit]
        result_single = result_single.sort_values(by=['Temp'])

        bins = result_single['Temp']
        pos = result_single['pos'].iloc[0]
        label_ppm = "pos#" + str(pos)
        # label_residual = "residual pos#" + str(pos)
        data_ppm = result_single['ppm']
        # data_residual = result_single['residual']


        axis.plot(bins, data_ppm, alpha=1, label=label_ppm, linewidth=1)

        #ax2.plot(bins, data_residual, alpha=1, label=label_residual, color = 'tab:orange', linewidth=1)


    plotTitle = title
    axis.set_title(plotTitle)

    # Show the major grid lines with dark grey lines
    axis.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)

    # Show the minor grid lines with very faint and almost transparent grey lines
    axis.minorticks_on()
    axis.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    axis.legend()
    #ax2.legend()

    fig.tight_layout()

    return fig




