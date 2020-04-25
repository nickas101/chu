import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def plot(df, df3, title):

    fig = Figure(figsize=(16, 8))
    axis = fig.add_subplot(1, 1, 1)

    axis.set_xlabel('Temperature, degC')
    axis.set_ylabel('Frequency, ppb')

    #ax2 = axis.twinx()

    units = df['pos'].unique().tolist()

    for unit in units:
        result_single = df[df['pos'] == unit]
        result_single = result_single.sort_values(by=['Temp'])

        result_single_3 = df3[df3['pos'] == unit]
        result_single_3 = result_single_3.sort_values(by=['Temp'])

        bins = result_single['Temp']
        bins_comp = result_single_3['Temp']
        pos = result_single['pos'].iloc[0]
        label_ppm = "pos#" + str(pos)
        label_comp = "comp pos#" + str(pos)
        data_ppb = result_single['ppb_norm']
        data_comp = result_single_3['residual_norm_ppb']


        axis.plot(bins, data_ppb, alpha=1, label=label_ppm, linewidth=1.5)
        axis.plot(bins_comp, data_comp, alpha=1, label=label_comp, linewidth=0.75)

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



