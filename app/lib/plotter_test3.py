import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from cycler import cycler
from matplotlib.figure import Figure
import matplotlib as plt


def plot(df, prediction, title):

    fig = Figure(figsize=(16, 8))
    axis = fig.add_subplot(1, 1, 1)

    axis.set_xlabel('Temperature, degC')
    axis.set_ylabel('Frequency, ppb')

    ax2 = axis.twinx()

    ax2.set_ylabel('Frequency, ppb')

    custom_cycler = (cycler(color=['b','g','r','c','m','y','k']))
    ax2.set_prop_cycle(custom_cycler)

    units = df['pos'].unique().tolist()

    for unit in units:
        # print(type(unit))
        # print(prediction[str(unit)])
        result_single = df[df['pos'] == unit]
        result_single = result_single.sort_values(by=['Temp'])

        temp_max = result_single['Temp'].max()
        temp_min = result_single['Temp'].min()

        bins = result_single['Temp']
        bins_prediction = prediction[(prediction['Temp'] < temp_max) & (prediction['Temp'] > temp_min)]['Temp']

        # print(bins_prediction)

        pos = result_single['pos'].iloc[0]

        label_ppm = "pos#" + str(pos)
        label_prediction = "prediction pos#" + str(pos)

        data_prediction = prediction[(prediction['Temp'] < temp_max) & (prediction['Temp'] > temp_min)][str(unit)]
        data_residual = result_single['residual_norm_ppb']

        # print(data_prediction)

        axis.plot(bins, data_residual, alpha=1, label=label_ppm, linewidth=1)
        # axis.plot(bins_prediction, data_prediction, alpha=1, label=label_prediction, linewidth=1.5)

        ax2.plot(bins_prediction, data_prediction, alpha=1, label=label_prediction, linestyle='--', linewidth=.75)

    plotTitle = title
    axis.set_title(plotTitle)

    # Show the major grid lines with dark grey lines
    axis.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)

    # Show the minor grid lines with very faint and almost transparent grey lines
    axis.minorticks_on()
    axis.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    # axis.legend()
    # ax2.legend()

    # plt.figlegend(lines, labels, loc='lower center', ncol=5, labelspacing=0.)

    # handles, labels = axis.get_legend_handles_labels()
    handles, labels = [(a + b) for a, b in zip(axis.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
    axis.legend(handles, labels, loc='upper left')
    # # fig.legend(handles, labels, loc='upper center')

    # fig.tight_layout()
    fig.set_tight_layout(True)

    return fig
