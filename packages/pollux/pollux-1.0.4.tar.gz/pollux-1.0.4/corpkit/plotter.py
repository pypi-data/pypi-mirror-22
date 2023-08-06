from __future__ import print_function
from corpkit.constants import STRINGTYPE, PYTHON_VERSION

def p_string_formatter(val, tex=False):
    if val < 0.001:
        if not tex:
            return 'p < 0.001'
        else:
            return r'p $<$ 0.001'
    else:
        return 'p = %s' % format(val, '.3f')

def plotter(df,
            title=False,
            kind='line',
            x_label=None,
            y_label=None,
            style='ggplot',
            figsize=(8, 4),
            save=False,
            legend_pos='best',
            reverse_legend='guess',
            num_to_plot=7,
            tex='try',
            colours='default',
            cumulative=False,
            pie_legend=True,
            partial_pie=False,
            show_totals=False,
            transparent=False,
            output_format='png',
            interactive=False,
            black_and_white=False,
            show_p_val=False,
            transpose=False,
            rot=False,
            **kwargs):
    """
    docstring at corpkit.interrogation.Results.visualise
    """
    import os
    try:
        from IPython.utils.shimmodule import ShimWarning
        import warnings
        warnings.simplefilter('ignore', ShimWarning)
    except:
        pass

    kwargs['rot'] = rot

    xtickspan = kwargs.pop('xtickspan', False)

    # prefer seaborn plotting
    try:
        import seaborn as sns
    except (ImportError, AttributeError):
        pass

    import matplotlib as mpl
    from matplotlib import rc

    if interactive:
        import matplotlib.pyplot as plt, mpld3
    else:
        import matplotlib.pyplot as plt

    import matplotlib.ticker as ticker
    
    import pandas
    from pandas import DataFrame, Series, MultiIndex

    from time import localtime, strftime

    if interactive:
        import mpld3
        import collections
        from mpld3 import plugins, utils
        from plugins import InteractiveLegendPlugin, HighlightLines

    have_mpldc = False
    try:
        from mpldatacursor import datacursor, HighlightingDataCursor
        have_mpldc = True
    except ImportError:
        pass

    # if the data was multiindexed, the default is a little different!
    from corpkit.interrogation import Results
    if isinstance(df.index, MultiIndex):
        import matplotlib.pyplot as nplt
        shape = kwargs.get('shape', 'auto')
        truncate = kwargs.get('truncate', 8)
        if shape == 'auto':
            shape = (int(len(df.index.levels[0]) / 2), 2)
        f, axes = nplt.subplots(*shape)
        for i, ((name, data), ax) in enumerate(zip(df.groupby(level=0), axes.flatten())):
            data = data.loc[name]
            if isinstance(truncate, int) and i > truncate:
                continue
            if kwargs.get('name_format'):
                name = kwargs.get('name_format').format(name)
            data = Results(matches=data)
            data.visualise(title=name,
            ax=ax,
            kind=kind,
            x_label=x_label,
            y_label=y_label,
            style=style,
            figsize=figsize,
            save=save,
            legend_pos=legend_pos,
            reverse_legend=reverse_legend,
            num_to_plot=num_to_plot,
            tex=tex,
            colours=colours,
            cumulative=cumulative,
            pie_legend=pie_legend,
            partial_pie=partial_pie,
            show_totals=show_totals,
            transparent=transparent,
            output_format=output_format,
            interactive=interactive,
            black_and_white=black_and_white,
            show_p_val=show_p_val,
            transpose=transpose,
            rot=rot)
        return nplt

    if not title:
        title = ''

    def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
        """remove extreme values from colourmap --- no pure white"""
        import matplotlib.colors as colors
        import numpy as np
        if isinstance(cmap, str):
            import matplotlib.pyplot as plt
            cmap = plt.get_cmap(cmap)
        new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
        return new_cmap

    def get_savename(imagefolder, save=False, title=False, ext='png'):
        """Come up with the savename for the image."""
        import os
        from corpkit.process import urlify

        # name as 
        if not ext.startswith('.'):
            ext = '.' + ext
        if isinstance(save, STRINGTYPE):
            savename = os.path.join(imagefolder, (urlify(save) + ext))
        #this 'else' is redundant now that title is obligatory
        else:
            if title:
                filename = urlify(title) + ext
                savename = os.path.join(imagefolder, filename)

        # remove duplicated ext
        if savename.endswith('%s%s' % (ext, ext)):
            savename = savename.replace('%s%s' % (ext, ext), ext, 1)
        return savename

    def rename_data_with_total(dataframe, was_series=False, using_tex=False, absolutes=True):
        """adds totals (abs, rel, keyness) to entry name strings"""
        if was_series:
            where_the_words_are = dataframe.index
        else:
            where_the_words_are = dataframe.columns
        the_labs = []
        for w in list(where_the_words_are):
            if not absolutes:
                if was_series:
                    perc = dataframe.T[w][0]
                else:
                    the_labs.append(w)
                    continue
                if using_tex:
                    the_labs.append('%s (%.2f\%%)' % (w, perc))
                else:
                    the_labs.append('%s (%.2f %%)' % (w, perc))
            else:
                if was_series:
                    score = dataframe.T[w].sum()
                else:
                    score = dataframe[w].sum()
                if using_tex:
                    the_labs.append('%s (n=%d)' % (w, score))
                else:
                    the_labs.append('%s (n=%d)' % (w, score))
        if not was_series:
            dataframe.columns = the_labs
        else:
            vals = list(dataframe[list(dataframe.columns)[0]].values)
            dataframe = pandas.DataFrame(vals, index=the_labs)
            dataframe.columns = ['Total']
        return dataframe

    def auto_explode(dataframe, tinput, was_series=False, num_to_plot=7):
        """give me a list of strings and i'll output explode option"""
        output = [0 for s in range(num_to_plot)]

        if was_series:
            l = list(dataframe.index)
        else:
            l = list(dataframe.columns)

        if isinstance(tinput, (STRINGTYPE, int)):
            tinput = [tinput]
        if isinstance(tinput, list):
            for i in tinput:
                if isinstance(i, STRINGTYPE):
                    index = l.index(i)
                else:
                    index = i
                output[index] = 0.1
        return output

    # get a few options from kwargs
    sbplt = kwargs.get('subplots', False)
    show_grid = kwargs.pop('grid', True)
    the_rotation = kwargs.get('rot', False)
    dragmode = kwargs.pop('draggable', False)
    leg_frame = kwargs.pop('legend_frame', True)
    leg_alpha = kwargs.pop('legend_alpha', 0.8)
    # auto set num to plot based on layout
    lo = kwargs.get('layout', None)
    if lo:
        num_to_plot = lo[0] * lo[1]

    if style == 'mpl-white':
        try:
            sns.set_style("whitegrid")
        except:
            pass
        style = 'matplotlib'

    if kwargs.get('savepath'):
        mpl.rcParams['savefig.directory'] = kwargs.get('savepath')
        kwargs.pop('savepath', None)

    mpl.rcParams['savefig.bbox'] = 'tight'
    mpl.rcParams.update({'figure.autolayout': True})

    # try to use tex
    # TO DO:
    # make some font kwargs here
    using_tex = False
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['text.latex.unicode'] = True
    
    if tex == 'try' or tex is True:
        try:
            rc('text', usetex=True)
            rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            using_tex = True
        except:
            matplotlib.rc('font', family='sans-serif') 
            matplotlib.rc('font', serif='Helvetica Neue') 
            matplotlib.rc('text', usetex='false') 
            rc('text', usetex=False)
    else:
        rc('text', usetex=False)  

    if interactive:
        using_tex = False 

    if show_totals is False:
        show_totals = 'none'

    # find out what kind of plot we're making, and enable
    # or disable interactive values if need be
    kwargs['kind'] = kind.lower()

    if interactive:
        if kwargs['kind'].startswith('bar'):
            interactive_types = [3]
        elif kwargs['kind'] == 'area':
            interactive_types = [2, 3]
        elif kwargs['kind'] == 'line':
            interactive_types = [2, 3]
        elif kwargs['kind'] == 'pie':
            interactive_types = None
            warnings.warn('Interactive plotting not yet available for pie plots.')
        else:
            interactive_types = [None]
    if interactive is False:
        interactive_types = [None]

    # find out if pie mode, add autopct format
    piemode = False
    if kind == 'pie':
        piemode = True
        # always the best spot for pie
        #if legend_pos == 'best':
            #legend_pos = 'lower left'
        if show_totals.endswith('plot') or show_totals.endswith('both'):
            kwargs['pctdistance'] = 0.6
            if using_tex:
                kwargs['autopct'] = r'%1.1f\%%'
            else:
                kwargs['autopct'] = '%1.1f%%'

    # copy data, make series into df
    dataframe = df.copy()
    if kind == 'heatmap':
        try:
            dataframe = dataframe.T
        except:
            pass
    was_series = False
    if isinstance(dataframe, Series):
        was_series = True
        if not cumulative:
            dataframe = DataFrame(dataframe)
        else:
            dataframe = DataFrame(dataframe.cumsum())
    else:
        # don't know if this is much good.
        if transpose:
            dataframe = dataframe.T
        if cumulative:
            dataframe = DataFrame(dataframe.cumsum())
        if len(list(dataframe.columns)) == 1:
            was_series = True
    
    def isint(x):
        try:
            a = float(x)
            b = int(a)
        except (ValueError, OverflowError):
            return False
        else:
            return a == b

    # set backend?
    output_formats = ['svgz', 'ps', 'emf', 'rgba', 'raw', 'pdf', 'svg', 'eps', 'png', 'pgf']
    if output_format not in output_formats:
        raise ValueError('%s output format not recognised. Must be: %s' % (output_format, ', '.join(output_formats)))
    
    # don't know if these are necessary
    if 'pdf' in output_format:
        plt.switch_backend(output_format) 
    if 'pgf' in output_format:
        plt.switch_backend(output_format)

    if num_to_plot == 'all':
        if was_series:
            if not piemode:
                num_to_plot = len(dataframe)
            else:
                num_to_plot = len(dataframe)
        else:
            if not piemode:
                num_to_plot = len(list(dataframe.columns))
            else:
                num_to_plot = len(dataframe.index)

    # explode pie, or remove if not piemode
    if piemode and not sbplt and kwargs.get('explode'):
        kwargs['explode'] = auto_explode(dataframe, 
                                        kwargs['explode'], 
                                        was_series=was_series, 
                                        num_to_plot=num_to_plot)
    else:
        kwargs.pop('explode', None)

    legend = kwargs.get('legend', True)

    #cut data short
    plotting_a_totals_column = False
    if was_series:
        if list(dataframe.columns)[0] != 'Total':
            try:
                can_be_ints = [int(x) for x in list(dataframe.index)]
                num_to_plot = len(dataframe)
            except:
                dataframe = dataframe[:num_to_plot]
        elif list(dataframe.columns)[0] == 'Total':
            plotting_a_totals_column = True
            if not 'legend' in kwargs:
                legend = False
            num_to_plot = len(dataframe)
    else:
        if transpose:
            dataframe = dataframe.head(num_to_plot)
        else:
            dataframe = dataframe.T.head(num_to_plot).T

    # remove stats fields, put p in entry text, etc.
    statfields = ['slope', 'intercept', 'r', 'p', 'stderr']
    try:
        dataframe = dataframe.drop(statfields, axis=1, errors='ignore')
    except:
        pass    
    try:
        dataframe.loc['p']
        there_are_p_vals = True
    except:
        there_are_p_vals = False
    if show_p_val:
        if there_are_p_vals:
            newnames = []
            for col in list(dataframe.columns):
                pval = dataframe[col]['p']
                pstr = p_string_formatter(pval)
                newname = '%s (%s)' % (col, pstr)
                newnames.append(newname)
            dataframe.columns = newnames
            dataframe.drop(statfields, axis=0, inplace = True, errors='ignore')
        else:
            warnings.warn('No p-values calculated to show.\n\nUse keep_stats kwarg while editing to generate these values.')
    else:
        if there_are_p_vals:
            dataframe.drop(statfields, axis=0, inplace=True, errors='ignore')

    # make and set y label
    absolutes = True
    if isinstance(dataframe, DataFrame):
        try:
            if not all([s.is_integer() for s in dataframe.iloc[0,:].values]):
                absolutes = False
        except:
            pass
    else:
        if not all([s.is_integer() for s in dataframe.values]):        
            absolutes = False

    # set defaults, with nothing for heatmap yet
    if colours is True or colours == 'default' or colours == 'Default':
        if kind != 'heatmap':
            colours = 'viridis'
        else:
            colours = 'default'
    
    # assume it's a single color, unless string denoting map
    cmap_or_c = 'color'
    if isinstance(colours, str):
        cmap_or_c = 'colormap'
    from matplotlib.colors import LinearSegmentedColormap
    if isinstance(colours, LinearSegmentedColormap):
        cmap_or_c = 'colormap'

    # for heatmaps, it's always a colormap
    if kind == 'heatmap':
        cmap_or_c = 'cmap'
        # if it's a defaulty string, set accordingly
        if isinstance(colours, str):
            if colours.lower().startswith('diverg'):
                colours = sns.diverging_palette(10, 133, as_cmap=True)

            # if default not set, do diverge for any df with a number < 0
            elif colours.lower() == 'default':
                mn = dataframe.min()
                if isinstance(mn, Series):
                    mn = mn.min()
                if mn < 0:
                    colours = sns.diverging_palette(10, 133, as_cmap=True)
                else:
                    colours = sns.light_palette("green", as_cmap=True)

    if 'seaborn' not in style:
        kwargs[cmap_or_c] = colours

    # reversing legend option
    if reverse_legend is True:
        rev_leg = True
    elif reverse_legend is False:
        rev_leg = False

    # show legend or don't, guess whether to reverse based on kind
    if kind in ['bar', 'barh', 'area', 'line', 'pie']:
        if was_series:
            legend = False
        if kind == 'pie':
            if pie_legend:
                legend = True
            else:
                legend = False
    if kind in ['barh', 'area']:
        if reverse_legend == 'guess':
            rev_leg = True
    if not 'rev_leg' in locals():
        rev_leg = False

    # the default legend placement
    if legend_pos is True:
        legend_pos = 'best'

    # cut dataframe if just_totals
    try:
        tst = dataframe['Combined total']
        dataframe = dataframe.head(num_to_plot)
    except:
        pass

    # no title for subplots because ugly,
    if title and not sbplt:
        kwargs['title'] = title
        
    # no interactive subplots yet:
    if sbplt and interactive:
        import warnings
        interactive = False
        warnings.warn('No interactive subplots yet, sorry.')
        return
        
    # not using pandas for labels or legend anymore.
    #kwargs['labels'] = None
    #kwargs['legend'] = False

    if legend:
        if num_to_plot > 6:
            if not kwargs.get('ncol'):
                kwargs['ncol'] = num_to_plot // 7
        # kwarg options go in leg_options
        leg_options = {'framealpha': leg_alpha,
                       'shadow': kwargs.get('shadow', False),
                       'ncol': kwargs.pop('ncol', 1)}    

        # determine legend position based on this dict
        if legend_pos:
            possible = {'best': 0, 'upper right': 1, 'upper left': 2, 'lower left': 3, 'lower right': 4, 
                        'right': 5, 'center left': 6, 'center right': 7, 'lower center': 8, 'upper center': 9, 
                        'center': 10, 'o r': 2, 'outside right': 2, 'outside upper right': 2, 
                        'outside center right': 'center left', 'outside lower right': 'lower left'}

            if isinstance(legend_pos, int):
                the_loc = legend_pos
            elif isinstance(legend_pos, str):
                try:
                    the_loc = possible[legend_pos]
                except KeyError:
                    raise KeyError('legend_pos value must be one of:\n%s\n or an int between 0-10.' %', '.join(list(possible.keys())))
            leg_options['loc'] = the_loc
            #weirdness needed for outside plot
            if legend_pos in ['o r', 'outside right', 'outside upper right']:
                leg_options['bbox_to_anchor'] = (1.02, 1)
            if legend_pos == 'outside center right':
                leg_options['bbox_to_anchor'] = (1.02, 0.5)
            if legend_pos == 'outside lower right':
                leg_options['loc'] == 'upper right'
                leg_options['bbox_to_anchor'] = (0.5, 0.5)
        
        # a bit of distance between legend and plot for outside legends
        if isinstance(legend_pos, str):
            if legend_pos.startswith('o'):
                leg_options['borderaxespad'] = 1

    if not piemode:
        if show_totals.endswith('both') or show_totals.endswith('legend'):
            dataframe = rename_data_with_total(dataframe, 
                                           was_series=was_series, 
                                           using_tex=using_tex, 
                                           absolutes=absolutes)
    else:
        if pie_legend:
            if show_totals.endswith('both') or show_totals.endswith('legend'):
                dataframe = rename_data_with_total(dataframe, 
                                           was_series=was_series, 
                                           using_tex=using_tex, 
                                           absolutes=absolutes)

    if piemode:
        if partial_pie:
            dataframe = dataframe / 100.0

    # some pie things
    if piemode:
        if not sbplt:
            kwargs['y'] = list(dataframe.columns)[0]
    
    def filler(df):
        pby = df.T.copy()
        for i in list(pby.columns):
            tot = pby[i].sum()
            pby[i] = pby[i] * 100.0 / tot
        return pby.T

    areamode = False
    if kind == 'area':
        areamode = True

    if legend is False:
        kwargs['legend'] = False

    # line highlighting option for interactive!
    if interactive:
        if 2 in interactive_types:
            if kind == 'line':
                kwargs['marker'] = ','
        if not piemode:
            kwargs['alpha'] = 0.1

    if kwargs.get('filled'):
        if areamode or kind.startswith('bar'):
            dataframe = filler(dataframe)
        kwargs.pop('filled', None)

    MARKERSIZE = 4
    COLORMAP = {
            0: {'marker': None, 'dash': (None,None)},
            1: {'marker': None, 'dash': [5,5]},
            2: {'marker': "o", 'dash': (None,None)},
            3: {'marker': None, 'dash': [1,3]},
            4: {'marker': "s", 'dash': [5,2,5,2,5,10]},
            5: {'marker': None, 'dash': [5,3,1,2,1,10]},
            6: {'marker': 'o', 'dash': (None,None)},
            7: {'marker': None, 'dash': [5,3,1,3]},
            8: {'marker': "1", 'dash': [1,3]},
            9: {'marker': "*", 'dash': [5,5]},
            10: {'marker': "2", 'dash': [5,2,5,2,5,10]},
            11: {'marker': "s", 'dash': (None,None)}
            }

    HATCHES = {
            0:  {'color': '#dfdfdf', 'hatch':"/"},
            1:  {'color': '#6f6f6f', 'hatch':"\\"},
            2:  {'color': 'b', 'hatch':"|"},
            3:  {'color': '#dfdfdf', 'hatch':"-"},
            4:  {'color': '#6f6f6f', 'hatch':"+"},
            5:  {'color': 'b', 'hatch':"x"}
            }

    if black_and_white:
        if kind == 'line':
            kwargs['linewidth'] = 1

        cmap = plt.get_cmap('Greys')
        new_cmap = truncate_colormap(cmap, 0.25, 0.95)
        if kind == 'bar':
            # darker if just one entry
            if len(dataframe.columns) == 1:
                new_cmap = truncate_colormap(cmap, 0.70, 0.90)
        kwargs[cmap_or_c] = new_cmap

    # remove things from kwargs if heatmap
    if kind == 'heatmap':
        hmargs = {'annot': kwargs.pop('annot', True),
              cmap_or_c: kwargs.pop(cmap_or_c, None),
              'fmt': kwargs.pop('fmt', ".2f"),
              'cbar': kwargs.pop('cbar', False)}

        for i in ['vmin', 'vmax', 'linewidths', 'linecolor',
                  'robust', 'center', 'cbar_kws', 'cbar_ax',
                  'square', 'mask', 'norm']:
            if i in kwargs.keys():
                hmargs[i] = kwargs.pop(i, None)

    class dummy_context_mgr():
        """a fake context for plotting without style
        perhaps made obsolete by 'classic' style in new mpl"""
        def __enter__(self):
            return None
        def __exit__(self, one, two, three):
            return False

    with plt.style.context((style)) if style != 'matplotlib' else dummy_context_mgr():

        kwargs.pop('filled', None)

        if not sbplt:
            # check if negative values, no stacked if so
            if areamode:
                if not kwargs.get('ax'):
                    kwargs['legend'] = False
                if dataframe.applymap(lambda x: x < 0.0).any().any():
                    kwargs['stacked'] = False
                    rev_leg = False
            if kind != 'heatmap':
                # turn off pie labels at the last minute
                if kind == 'pie' and pie_legend:
                    kwargs['labels'] = None
                    kwargs['autopct'] = '%.2f'
                if kind == 'pie':
                    kwargs.pop('color', None)
                    kwargs.pop('alpha', None)
                ax = dataframe.plot(figsize=figsize, **kwargs)
            else:
                fg = plt.figure(figsize=figsize)
                if title:
                    plt.title(title)
                ax = kwargs.get('ax', plt.axes())
                tmp = sns.heatmap(dataframe, ax=ax, **hmargs)
                ax.set_title(title)
                for item in tmp.get_yticklabels():
                    item.set_rotation(0)
                plt.close(fg)

            if areamode and not kwargs.get('ax'):
                handles, labels = plt.gca().get_legend_handles_labels()
                del handles
                del labels

            if x_label:
                ax.set_xlabel(x_label)
            if y_label:
                ax.set_ylabel(y_label)

        else:
            if not kwargs.get('layout'):
                plt.gcf().set_tight_layout(False)

            if kind != 'heatmap':
                if kind == 'pie' and pie_legend:
                    kwargs['labels'] = None
                    kwargs['autopct'] = '%.2f'
                if kind == 'pie':
                    kwargs.pop('color', None)
                    kwargs.pop('alpha', None)
                ax = dataframe.plot(figsize=figsize, **kwargs)
            else:
                plt.figure(figsize=figsize)
                if title:
                    plt.title(title)
                ax = plt.axes()
                sns.heatmap(dataframe, ax=ax, **hmargs)
                plt.xticks(rotation=0)
                plt.yticks(rotation=0)

        def rotate_degrees(rotation, labels):
            if rotation is None:
                if max(labels, key=len) > 6:
                    return 45
                else:
                    return 0
            elif rotation is False:
                return 0
            elif rotation is True:
                return 45
            else:
                return rotation
        
        if sbplt:
            if 'layout' not in kwargs:
                axes = [l for l in ax]
            else:
                axes = []
                cols = [l for l in ax]
                for col in cols:
                    for bit in col:
                        axes.append(bit)
            for index, a in enumerate(axes):
                if xtickspan is not False:
                    a.xaxis.set_major_locator(ticker.MultipleLocator(xtickspan))
                labels = [item.get_text() for item in a.get_xticklabels()]
                rotation = rotate_degrees(the_rotation, labels)                
                try:
                    if the_rotation == 0:
                        ax.set_xticklabels(labels, rotation=rotation, ha='center')
                    else:
                        ax.set_xticklabels(labels, rotation=rotation, ha='right')
                except AttributeError:
                    pass
        else:
            if kind == 'heatmap':
                labels = [item.get_text() for item in ax.get_xticklabels()]
                rotation = rotate_degrees(the_rotation, labels)
                if the_rotation == 0:
                    ax.set_xticklabels(labels, rotation=rotation, ha='center')
                else:
                    ax.set_xticklabels(labels, rotation=rotation, ha='right')

        if transparent:
            plt.gcf().patch.set_facecolor('white')
            plt.gcf().patch.set_alpha(0)

        if black_and_white:
            if kind == 'line':
                # white background
                # change everything to black and white with interesting dashes and markers
                c = 0
                for line in ax.get_lines():
                    line.set_color('black')
                    #line.set_width(1)
                    line.set_dashes(COLORMAP[c]['dash'])
                    line.set_marker(COLORMAP[c]['marker'])
                    line.set_markersize(MARKERSIZE)
                    c += 1
                    if c == len(list(COLORMAP.keys())):
                        c = 0

        # draw legend with proper placement etc
        if legend:
            if not piemode and not sbplt and kind != 'heatmap':
                if 3 not in interactive_types:
                    handles, labels = plt.gca().get_legend_handles_labels()
                    # area doubles the handles and labels. this removes half:
                    #if areamode:
                    #    handles = handles[-len(handles) / 2:]
                    #    labels = labels[-len(labels) / 2:]
                    if rev_leg:
                        handles = handles[::-1]
                        labels = labels[::-1]
                    if kwargs.get('ax'):
                        lgd = plt.gca().legend(handles, labels, **leg_options)
                        ax.get_legend().draw_frame(leg_frame)
                    else:
                        lgd = plt.legend(handles, labels, **leg_options)
                        lgd.draw_frame(leg_frame)

    if interactive:
        # 1 = highlight lines
        # 2 = line labels
        # 3 = legend switches
        ax = plt.gca()
        # fails for piemode
        lines = ax.lines
        handles, labels = plt.gca().get_legend_handles_labels()
        if 1 in interactive_types:
            plugins.connect(plt.gcf(), HighlightLines(lines))

        if 3 in interactive_types:
            plugins.connect(plt.gcf(), InteractiveLegendPlugin(lines, labels, alpha_unsel=0.0))

        for i, l in enumerate(lines):
            y_vals = l.get_ydata()
            x_vals = l.get_xdata()
            x_vals = [str(x) for x in x_vals]
            if absolutes:
                ls = ['%s (%s: %d)' % (labels[i], x_val, y_val) for x_val, y_val in zip(x_vals, y_vals)]
            else:
                ls = ['%s (%s: %.2f%%)' % (labels[i], x_val, y_val) for x_val, y_val in zip(x_vals, y_vals)]
            if 2 in interactive_types:
                #if 'kind' in kwargs and kwargs['kind'] == 'area':
                tooltip_line = mpld3.plugins.LineLabelTooltip(lines[i], labels[i])
                mpld3.plugins.connect(plt.gcf(), tooltip_line)
                #else:
                if kind == 'line':
                    tooltip_point = mpld3.plugins.PointLabelTooltip(l, labels = ls)
                    mpld3.plugins.connect(plt.gcf(), tooltip_point)
        
    if piemode:
        if not sbplt:
            plt.axis('equal')
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

    y_l = False
    if not absolutes:
        y_l = 'Percentage'
    else:
        y_l = 'Absolute frequency'

    # hacky: turn legend into subplot titles :)
    if sbplt:
        # title the big plot
        #plt.gca().suptitle(title, fontsize = 16)
        #plt.subplots_adjust(top=0.9)
        # get all axes
        if 'layout' not in kwargs:
            axes = [l for index, l in enumerate(ax)]
        else:
            axes = []
            cols = [l for index, l in enumerate(ax)]
            for col in cols:
                for bit in col:
                    axes.append(bit)
    
        # set subplot titles
        for index, a in enumerate(axes):
            try:
                titletext = list(dataframe.columns)[index]
            except:
                pass
            a.set_title(titletext)
            try:
                a.legend_.remove()
            except:
                pass
            #try:
            #    from matplotlib.ticker import MaxNLocator
            #    from corpkit.process import is_number
            #    indx = list(dataframe.index)
            #    if all([is_number(qq) for qq in indx]):
            #        ax.get_xaxis().set_major_locator(MaxNLocator(integer=True))
            #except:
            #    pass
            # remove axis labels for pie plots
            if piemode:
                a.axes.get_xaxis().set_visible(False)
                a.axes.get_yaxis().set_visible(False)
                a.axis('equal')

            a.grid(b=show_grid)
        
    # add sums to bar graphs and pie graphs
    # doubled right now, no matter

    if not sbplt:
        
        # show grid
        ax.grid(b=show_grid)

        if kind.startswith('bar'):
            width = ax.containers[0][0].get_width()

    if was_series:
        the_y_limit = plt.ylim()[1]
        if show_totals.endswith('plot') or show_totals.endswith('both'):
            # make plot a bit higher if putting these totals on it
            plt.ylim([0,the_y_limit * 1.05])
            for i, label in enumerate(list(dataframe.index)):
                if len(dataframe.loc[label]) == 1:
                    score = dataframe.loc[label][0]
                else:
                    if absolutes:
                        score = dataframe.loc[label].sum()
                    else:
                        #import warnings
                        #warnings.warn("It's not possible to determine total percentage from individual percentages.")
                        continue
                if not absolutes:
                    plt.annotate('%.2f' % score, (i, score), ha = 'center', va = 'bottom')
                else:
                    plt.annotate(score, (i, score), ha = 'center', va = 'bottom')
    else:
        the_y_limit = plt.ylim()[1]
        if show_totals.endswith('plot') or show_totals.endswith('both'):
            for i, label in enumerate(list(dataframe.columns)):
                if len(dataframe[label]) == 1:
                    score = dataframe[label][0]
                else:
                    if absolutes:
                        score = dataframe[label].sum()
                    else:
                        #import warnings
                        #warnings.warn("It's not possible to determine total percentage from individual percentages.")
                        continue
                if not absolutes:
                    plt.annotate('%.2f' % score, (i, score), ha='center', va='bottom')
                else:
                    plt.annotate(score, (i, score), ha='center', va='bottom')        

    if not kwargs.get('layout') and not sbplt and not kwargs.get('ax'):
        plt.tight_layout()
    if kwargs.get('ax'):
        try:
            plt.gcf().set_tight_layout(False)
        except:
            pass
        try:
            plt.set_tight_layout(False)
        except:
            pass

    if save:
        imagefolder = 'images'
        savename = get_savename(imagefolder, save=save, title=title, ext=output_format)

        if not os.path.isdir(imagefolder):
            os.makedirs(imagefolder)

        # save image and get on with our lives
        if legend_pos.startswith('o') and not sbplt:
            plt.gcf().savefig(savename, dpi=150, bbox_extra_artists=(lgd,), 
                              bbox_inches='tight', format=output_format)
        else:
            plt.gcf().savefig(savename, dpi=150, format=output_format)
        time = strftime("%H:%M:%S", localtime())
        if os.path.isfile(savename):
            print('\n' + time + ": " + savename + " created.")
        else:
            raise ValueError("Error making %s." % savename)

    if dragmode:
        plt.legend().draggable()

    if sbplt:
        plt.subplots_adjust(right=.8)
        plt.subplots_adjust(left=.1)

    # add DataCursor to notebook backend if possible
    if have_mpldc:
        if kind == 'line':
            HighlightingDataCursor(plt.gca().get_lines(), highlight_width=4, highlight_color = False,
                    formatter=lambda **kwargs: '%s: %s' % (kwargs['label'], "{0:.3f}".format(kwargs['y'])))
        else:
            datacursor(formatter=lambda **kwargs: '%s: %s' % (kwargs['label'], "{0:.3f}".format(kwargs['height'])))

    if interactive:
        plt.subplots_adjust(right=.8)
        plt.subplots_adjust(left=.1)
        try:
            ax.legend_.remove()
        except:
            pass
        return mpld3.display()
    else:
        return plt

def multiplotter(df, main_params={}, sub_params={}, layout=4, split_subplots=True, **kwargs):
    """
    Plot a big chart and its subplots together
    :param main_params: a dict of arguments for the big plot
    :param sub_params: a dict of arguments for the small plot
    
    """
    from corpkit.interrogation import Results
    import matplotlib.pyplot as plt
    import pandas as pd
    axes = []

    if isinstance(df, Results):
        df = df.results

    df2 = sub_params.pop('data', df.copy())
    #todo?
    if isinstance(df2, Results):
        df2 = df2.table()

    # add more cool layouts here
    # and figure out a nice way to access them other than numbers...
    
    if not isinstance(layout, list):
        from corpkit.layouts import layouts
        layout = layouts.get(layout, False)
        if layout is False:
            raise ValueError("Layout not found")

    kinda = main_params.pop('kind', 'area')
    kindb = sub_params.pop('kind', 'line')
    tpa = main_params.pop('transpose', False)
    tpb = sub_params.pop('transpose', False)
    if not split_subplots:
        numtoplot = main_params.pop('num_to_plot', 7)
    else:
        numtoplot = main_params.pop('num_to_plot', len(layout) - 1)

    ntpb = sub_params.pop('num_to_plot', 'all')
    sharex = sub_params.pop('sharex', True)
    sharey = sub_params.pop('sharey', False)
    if kindb == 'pie':
        piecol = sub_params.pop('colours', 'default')
    coloursb = sub_params.pop('colours', 'default')
    fig = plt.figure()
    d2_series = False
    
    size = kwargs.pop('figsize', (10, 4))

    show_p = kwargs.pop('show_p_val', False)

    main_params.update(kwargs)
    sub_params.update(kwargs)
    
    for i, (nrows, ncols, plot_number) in enumerate(layout, start=-1):
        if tpb:
            df2 = df2.T
        if hasattr(df2, 'columns') and i >= len(df2.columns):
            continue
        ax = fig.add_subplot(nrows, ncols, plot_number)

        if i == -1:
            df.visualise(kind=kinda, ax=ax, transpose=tpa,
                         num_to_plot=numtoplot, **main_params)
            if kinda in ['bar', 'hist', 'barh']:
                import matplotlib as mpl
                all_col = []
                colmap = []
                rects = [r for r in ax.get_children() if isinstance(r, mpl.patches.Rectangle)]
                for r in rects:
                    all_col.append(r._facecolor)
                    if r._facecolor not in colmap:
                        colmap.append(r._facecolor)
                try:
                    colmap = {list(df.columns)[i]: x for i, x in enumerate(colmap[:len(df.columns)])}
                except AttributeError:
                    colmap = {list(df.index)[i]: x for i, x in enumerate(colmap[:len(df.index)])}
            else:
                try:
                    colmap = {list(df.columns)[i]: l.get_color() for i, l in enumerate(ax.get_lines())}
                except AttributeError:
                    colmap = {list(df.index)[i]: l.get_color() for i, l in enumerate(ax.get_lines())}
        else:
            if colmap and kindb != 'pie' and split_subplots:
                try:
                    name = df2.iloc[:, i].name
                    coloursb = colmap[name]
                except IndexError:
                    coloursb = 'gray'
                except KeyError:
                    coloursb = 'gray'
                except:
                    # if series
                    name = df2.name
                    coloursb = 'gray'
                    d2_series = True

            if split_subplots:
                if kindb == 'pie':
                    sub_params['colours'] = piecol
                else:
                    sub_params['colours'] = coloursb

            if d2_series or not split_subplots:
                to_show = df2
            else:
                to_show = df2.iloc[:, i]

            if show_p and isinstance(to_show, pd.Series):
                to_show.name = '%s (%s)' % (name, p_string_formatter(to_show['p'], tex=kwargs.get('tex', True)))
            elif show_p and isinstance(to_show, pd.DataFrame):
                to_show.columns = ['%s (%s)' % (nn, p_string_formatter(to_show.loc['p', n], tex=kwargs.get('tex', True))) for n in to_show.columns]

            to_show.visualise(kind=kindb,
                              ax=ax,
                              sharex=sharex,
                              sharey=sharey,
                              num_to_plot=ntpb,
                              **sub_params)
            
            if not d2_series and split_subplots:
                ax.set_title(to_show.name)
        
    wspace = kwargs.get('wspace', .2)
    hspace = kwargs.get('hspace', .5)

    fig.subplots_adjust(bottom=0.025, left=0.025, top=0.975, right=0.975,
                        wspace=wspace, hspace=hspace)

    fig.set_size_inches(size)
    try:
        plt.set_size_inches(size)
    except:
        pass
    if kwargs.get('save'):
        import os
        from corpkit.process import urlify
        savepath = os.path.join('images', urlify(kwargs['save']) + '.png')
        fig.savefig(savepath, dpi=150)
    plt.tight_layout()
    return plt
    
