"""Provide definitions of some auxiliary funtions that
are used during analysis

"""

import matplotlib
import numpy as np
import math
SPINE_COLOR = 'gray'


def return_uniques(seq, idfun=None):
    """Return list of unique elements from
    list ``seq``

    """

    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def set_plot_parameters(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Original source: http://nipunbatra.github.io/2014/08/latexify/

    **Parameters**
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    assert(columns in [1, 2])

    if fig_width is None:
        fig_width = 1.5 * 3.39 if columns == 1 else 6.9  # width in inches

    if fig_height is None:
        golden_mean = (math.sqrt(5) - 1.0) / 2.0    # Aesthetic ratio
        fig_height = fig_width * golden_mean  # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height +
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES
    main_size = 8
    params = {'backend': 'ps',
              'text.latex.preamble': ['\\usepackage{gensymb}'],
              'axes.labelsize': main_size,  # fontsize for x and y labels
              'axes.titlesize': main_size + 1,
              'font.size': main_size,  # was 10
              'legend.fontsize': main_size + 1,  # was 10
              'xtick.labelsize': main_size,
              'ytick.labelsize': main_size,
              'text.usetex': True,
              'figure.figsize': [fig_width, fig_height],
              'font.family': 'serif'
              }

    matplotlib.rcParams.update(params)


def format_axes(ax):
    """Format axis of the plot into more readable layout.

    Call before saving a plot.

    Source of the function: http://nipunbatra.github.io/2014/08/latexify/

    """

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax


def main_color():
    """Return main color used in plots as a HEX string code

    """
    return('#CC6677')


def secondary_color():
    """Return secondary color used in plots as a HEX string code

    """
    return('#4477AA')


def color_pallete(n):
    """Return ``n`` th color from a pallete of distinc, color--blind proof
     colors.
     ``n`` can be at most 13

    """

    if n > 12:
        return None
        # TODO: raise error here
    idx = np.linspace(1, 12, n, dtype=int).tolist()

    colors = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77',
              '#CC6677', '#882255', '#AA4499', '#661100', '#6699CC', '#AA4466',
              '#4477AA']
    return [colors[i] for i in idx]


def slice_SIPP(variable, start, stop):
    """creates a column name for given `variable` beginnig from `start` and endng at `stop`. The output format
    it *variable_wave-month*. Used to index SIPP data.

    **input**: `start` and `stop` indicate which month of which wave to extract. If supplied as list, then interpreted as
    firt element of the list being wave and second month. If supplied as a integer, then it is treated as
    number of wave-month pariods starting from wave 1 and month 1 (e.g. 8 means wave 2 month 4).

    **return** slice of columns from `start` to `stop` that can be used directly to index pandas data frame with SIPP data

    """
    if isinstance(start, int):
        beginn_wave = math.ceil(start / 4)
        beginn_month = (start - 1) % 4 + 1
    elif (isinstance(start, tuple) or isinstance(start, list)):
        beginn_wave = start[0]
        beginn_month = start[1]
    else:
        print("unknown type of start idnicator")

    if isinstance(stop, int):
        end_wave = math.ceil(stop / 4)
        end_month = (stop - 1) % 4 + 1
    elif (isinstance(stop, tuple) or isinstance(stop, list)):
        end_wave = stop[0]
        end_month = stop[1]
    else:
        print("unknown type of stop indicator")

    a = slice('{}_wave{}-month{}'.format(variable, beginn_wave, beginn_month),
              '{}_wave{}-month{}'.format(variable, end_wave, end_month))
    return a
