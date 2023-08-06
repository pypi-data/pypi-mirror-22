"""
A corpkit interpreter, with natural language commands.
"""

from __future__ import print_function

help_text = "\nThis is a dedicated interpreter for corpkit, a tool for creating, searching\n" \
            "and visualising corpora. It works through a combination of objects and commands:\n\n" \
            "Objects:\n\n" \
            " +---------------+-----------------------------------------------+ \n"\
            " | Object        | Contains                                      | \n"\
            " +===============+===============================================+ \n"\
            " | `corpus`      | Dataset selected for parsing or searching     | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `results`     | Search output                                 | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `edited`      | Results after sorting, editing or calculating | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `concordance` | Concordance lines from search                 | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `features`    | General linguistic features of corpus         | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `wordclasses` | Distribution of word classes in corpus        | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `postags`     | Distribution of POS tags in corpus            | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `figure`      | Plotted data                                  | \n"\
            " +---------------+-----------------------------------------------+ \n"\
            " | `query`       | Values used to perform search or edit         | \n"\
            " +---------------+-----------------------------------------------+ "\
            "\n\nCommand examples:\n\n" \
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | Command         | Purpose                                                      | Syntax                                                                                     |  \n"\
            " +=================+==============================================================+============================================================================================+  \n"\
            " | `new`           | Make a new project                                           | `new project <name>`                                                                       |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `set`           | Set current corpus                                           | `set <corpusname>`                                                                         |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `parse`         | Parse corpus                                                 | `parse corpus with [options]*`                                                             |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `search`        | Search a corpus for linguistic feature, generate concordance | `search corpus for [feature matching pattern]* showing [feature]* with [options]*`         |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `edit`          | Edit results or edited results                               | `edit result by [skipping subcorpora/entries matching pattern]* with [options]*`           |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `calculate`     | Calculate relative frequencies, keyness, etc.                | `calculate result/edited as operation of denominator`                                      |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `sort`          | Sort results or concordance                                  | `sort result/concordance by value`                                                         |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `plot`          | Visualise result or edited result                            | `plot result/edited as line chart with [options]*`                                         |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `show`          | Show any object                                              | `show object`                                                                              |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `annotate`      | Add annotations to corpus based on search results            | `annotate all with field as <fieldname> and value as m`                                    |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `unannotate`    | Delete annotation fields from corpus                         | `unannotate <fieldname> field`                                                             |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `sample`        | Get a random sample of subcorpora or files from a corpus     | `sample 5 subcorpora of corpus`                                                            |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `call`          | Name an object (i.e. make a variable)                        | `call object '<name>'`                                                                     |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `export`        | Export result, edited result or concordance to string/file   | `export result to string/csv/latex/file <filename>`                                        |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `save`          | Save data to disk                                            | `save object to <filename>`                                                                |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `load`          | Load data from disk                                          | `load object as result`                                                                    |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `store`         | Store something in memory                                    | `store object as <name>`                                                                   |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `fetch`         | Fetch something from memory                                  | `fetch <name> as object`                                                                   |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `help`          | Get help on an object or command                             | `help command/object`                                                                      |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `history`       | See previously entered commands                              | `history`                                                                                  |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `ipython`       | Enter IPython with objects available                         | `ipython`                                                                                  |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `py`            | Execute Python code                                          | `py 'print('hello world')'`                                                                |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            " | `!`             | Run a line of bash shell                                     | `!ls -al data`                                                                             |  \n"\
            " +-----------------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------+  \n"\
            "\nMore information:\n\nYou can access more specific help by entering corpkit, then by doing 'help <command>', or by visiting\n" \
            "http://corpkit.readthedocs.io/en/latest\n\n" \
            "For help on viewing results and concordances, hit '?' when in the viewing mode.\n\n"

from corpkit.constants import STRINGTYPE, PYTHON_VERSION, INPUTFUNC, OPENER, transshow, transobjs

import os
import traceback
import pandas as pd

try:
    import gnureadline as readline
except ImportError:
    import readline

import atexit

# todo: fix these imports
import corpkit
from corpkit import *
from corpkit.corpus import Corpus
from corpkit.constants import transshow, transobjs
from corpkit.interrogation import Results
from corpkit.other import load
from corpkit.completer import Completer

import warnings
warnings.simplefilter(action="ignore", category=UserWarning)

# pandas display setup, though this is rarely used when LESS
# and tabview are available
size = pd.util.terminal.get_terminal_size()
pd.set_option('display.max_rows', 0)
pd.set_option('display.max_columns', 0)
pd.set_option('display.float_format', lambda x: '{:,.3f}'.format(x))

# allow ctrl-r, etc
readline.parse_and_bind('set editing-mode vi')

# command completion
poss = ['testing', 'search', 'concordance']

try:
    import gnureadline as readline
except ImportError:
    import readline as readline

completer = Completer(poss)

readline.set_completer(completer.complete)

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

# this code makes it possible to remember history from previous sessions
history_path = os.path.expanduser("~/.pyhistory")

def save_history(history_path=history_path):
    """
    On exit, add previous commands to history file
    """
    try:
        import gnureadline as readline
    except ImportError:
        import readline as readline
    try:
        readline.remove_history_item(readline.get_current_history_length() - 1)
    except ValueError:
        pass
    readline.write_history_file(history_path)

if os.path.exists(history_path):
    try:
        readline.set_history_length(1000)
        readline.read_history_file(history_path)
        readline.set_history_length(1000)
    except IOError:
        pass

# bind to exit
atexit.register(save_history)

# tab completion

# ctrl r search
#readline.parse_and_bind("bind ^R em-inc-search-prev")

del os, atexit, save_history, history_path
#del rlcompleter

class Objects(object):
    """
    In here are all of the major variables being used by the interpreter
    This is much nicer than using globals
    """

    def __init__(self):

        # get dict of all possible wordlists
        from corpkit.dictionaries.roles import roles
        from corpkit.dictionaries.wordlists import wordlists
        from corpkit.dictionaries.process_types import processes
        from corpkit.dictionaries.verblist import allverbs
        from collections import defaultdict
        wl = wordlists._asdict()
        try:
            wl.update(roles.__dict__)
        except AttributeError:
            wl.update(roles._asdict())
        wl.update(processes.__dict__)
        wl['anyverb'] = allverbs

        self._protected = ['result', 'previous', 'edited', 'corpus', 'concordance',
                          'query', 'features', 'postags', 'wordclasses', 'stored',
                          'figure', 'totals', 'wordlists', 'wordlist', 'matching',
                          'showing', 'excluding', 'not', 'as', 'with', 'and', 'by',
                          'm', 'l', 'r', 'conc', 'keeping', 'skipping', 'entries', 'subcorpora',
                          'merging', 'k', 'sampled',
                          '_in_a_project', '_old_searches',
                          '_conc_colours', '_conc_kwargs',
                          '_interactive', '_decimal', '_protected']
                          
        # main variables the user might access
        self.result = None
        self.previous = None
        self.edited = None
        self.corpus = None
        self.concordance = None
        self.query = None
        self.features = None
        self.sampled = None
        self.postags = None
        self.wordclasses = None
        self.stored = {}
        self.figure = None
        self.totals = None
        self.wordlists = wl
        self.wordlist = None
        self.named = {}
        self.just = {}
        self.skip = {}
        self.symbolic = False
        self._docker = False
        self.max_cols = None
        self.max_rows = None
        self._comma = False
        self._last_shown = None
        self._token_show_format = ['mw']

        # system toggles and references to older data
        self._in_a_project = None
        self._old_searches = []
        self._conc_colours = defaultdict(dict)
        self._conc_kwargs = {'n': 999}

        # user settings  (more to come?)
        self._interactive = True
        self._decimal = 3
        self._annotation_unlocked = False



    def _get(self, name):
        """
        Get an object, item from store or wordlist
        """
        if name.startswith('wordlist') or name.startswith('stored'):
            ob, attr = name.split('.', 1) if '.' in name else name.split(':', 1)
            return ob, getattr(self, ob).get(attr)
        feats = ['features', 'postags', 'wordclasses']
        if any(name.startswith(i) for i in feats):
            corpus = self.corpus
            attr = name.split('.', 1)
            if len(attr) == 1:
                return name, getattr(corpus, name)
            else:
                bit = attr[1].upper() if attr[0] == 'postags' else attr[1].title()
                data = getattr(corpus, attr[0])[bit]
                return 'series', data
        if name in self._protected:
            return name, getattr(self, name, None)
        else:
            return self.named.get(name, (None, None))

def interpreter(debug=False,
                fromscript=False,
                quiet=False,
                python_c_mode=False,
                profile=False,
                loadcurrent=False,
                docker=False):

    import os

    allig = '\n   Welcome!\n'
    allig += "               .-._   _ _ _ _ _ _ _ _\n    " \
             ".-''-.__.-'00  '-' ' ' ' ' ' ' ' '-.\n    " \
             "'.___ '    .   .--_'-' '-' '-' _'-' '._\n    " \
             "V: V 'vv-'   '_   '.       .'  _..' '.'.\n    "\
             "  '=.____.=_.--'   :_.__.__:_   '.   : :\n    "\
             "          (((____.-'        '-.  /   : :\n    "\
             "                            (((-'\ .' /\n    "\
             "                          _____..'  .'\n    "\
             "                         '-._____.-'\n"

    objs = Objects()

    if docker:
        objs._docker = docker

    # basic way to check that we're currently in a project, because i'm lazy
    def check_in_project():
        import os
        proj_dirs = ['data', 'saved_interrogations', 'exported']
        if all(x in os.listdir('.') for x in proj_dirs):
            return True

        cpkt_dirs = ['API-README.md', 'corpkit', 'data', 'rst_docs']
        if all(x in os.listdir('.') for x in cpkt_dirs):
            return True

        return False

    def generate_outprint():
        """
        Text to appear when switching to IPython
        """
        s = 'Switched to IPython ... defined variables:\n\n\t'
        s += 'corpus, results, concordance, edited ...\n\n\tType "quit" to return to corpkit environment'
        return s

    def read_script(fname):
        """
        If a sript was passed to corpkit, get lines in it, minus comments
        """
        with OPENER(fname, 'r') as fo:
            data = fo.read()
        data = data.splitlines()
        data = [i for i in data if i.strip() and i.strip()[0] != '#']

        return list(reversed(data))

    def helper(tokens):
        """
        Give user help if they enter a command alone
        """
        func = get_command.get(tokens[0], False)

        if not func:
            print('Not recognised: %s' % tokens[0])
            return

        print(getattr(func, '__doc__', 'Not written yet, sorry.'))

    def switch_to_ipython(args):
        from IPython import embed
        from IPython.terminal.embed import InteractiveShellEmbed
        s = generate_outprint()
        for k, v in objs.__dict__.items():
            if not k.startswith('_'):
                locals()[k] = v
        for k, v in objs.named.items():
            locals()[k] = v

        ret = InteractiveShellEmbed(header=s,
                    babaii='babaii',
                    #colors='Linux',
                    exit_msg='Switching back to corpkit environment ...',
                    local_ns=locals())
        cc = ret()

    def switch_to_jupyter(args):
        comm = ["jupyter", "notebook"]
        import subprocess
        if args:
            import os
            nbfile = args[-1]
            if not nbfile.endswith('.ipynb'):
                nbfile = nbfile + '.ipynb'
            if os.path.isfile(nbfile):
                comm.append(nbfile)
        subprocess.call(comm)            

    def switch_to_gui(args):
        import subprocess
        import os
        print('Loading graphical interface ... ')
        subprocess.call(["python", "-m", 'corpkit.gui', os.getcwd()])

    def show_concordance(tokens, conc_obj=False, start_pos=False):
        import pydoc
        kwargs = process_kwargs(tokens)
        show = kwargs.pop('m', False)
        if not show:
            show = objs._token_show_format
        else:
            objs._token_show_format = show
        if conc_obj is False:
            conc_obj = objs._get('result')[1]
        #TODO: n, columns, etc.

        objs.concordance = conc_obj.conc(show=show, **kwargs)
        # retrieve the correct concordances, so we can colour them
        found_the_conc = next((i for i, c in enumerate(objs._old_searches) \
                               if c.equals(objs.result)), None)
        if found_the_conc is None:
            return
        new_ix = []
        from colorama import Fore, Back, Style, init
        thisc = objs._conc_colours[found_the_conc]
        objs._last_shown = 'conc'
        #.drop(objs._conc_kwargs.get('columns', []) axis=1, errors='ignore')
        objs.concordance.tabview(colours=thisc, start_pos=False)
        return

    def show_table(obj, objtype=False, start_pos=False):
        """
        Print or tabview a Pandas object
        """
        if objs._interactive:
            import tabview
            showfunc = tabview.view
            kwa = {'column_width': 10, 'align_right': True}
        else:
            showfunc = print
            kwa = {}

        if start_pos:
            kwa['start_pos'] = start_pos

        #if not getattr(obj, 'data', False):
        #    obj = getattr(obj, 'results', obj)
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            df = obj.round(objs._decimal)
            if isinstance(obj, pd.DataFrame):
                df = df.iloc[:objs.max_rows,:objs.max_cols]
            else:
                df = df[:objs.max_rows]

            if objs._comma:
                if isinstance(obj, pd.DataFrame):
                    df = df.applymap(lambda x: '{:,}'.format(x))
                else:
                    df = df.apply(lambda x: '{:,}'.format(x))
            #if showfunc == tabview.view:
            #    df = df.astype(str).apply(lambda x: x.str.rjust(len(x.name), ' '))
            for poss in ['f', 'file']:
                if poss in df.columns:
                    import os
                    df[poss] = df[poss].apply(os.path.basename)

            showfunc(df, **kwa)
            return
        # not sure what might be here
        elif obj:
            try:
                df = obj.round(objs._decimal)
            except:
                df = obj
            try:
                df = df[:objs.max_rows,:objs.max_cols]
            except:
                pass
            showfunc(df[:objs.max_rows,:objs.max_cols], **kwa)
            return
        #else:
        #    if isinstance(objs._get(command)[1], (pd.DataFrame, pd.Series)):
        #        showfunc(objs._get(command)[1].round(objs._decimal), **kwa)
        #        return

    def single_command_print(command):
        """
        If the user enters just a single token, show them that token
        This function also processes multiword tokens sometimes, which is inconsistent.
        """

        helpable = ['calculate', 'plot', 'search', 'fetch', 'store', 'save', 'edit',
                    'export', 'sort', 'load', 'mark', 'del', 'annotate', 'unannotate',
                    'sample', 'call']

        if isinstance(command, list) and len(command) == 1 and command[0] in helpable:
            helper(command)

        args = []
        if isinstance(command, list):
            args = command[1:]
            command = command[0]

        if command in objs.named.keys():
            objtype, obj = objs.named.get(command)
            if isinstance(obj, str):
                print('%s: %s' % (command, obj))
                return
            elif objtype == 'eval':
                print('%s: ' % command, obj)
        else:
            objtype, obj = objs._get(command)
            if not objtype:
                objtype = command

        if objtype == 'ls':
            import os
            print('\n'.join(os.listdir('.')))

        if objtype == 'clear':
            try:
                from blessings import Terminal
                terminal = Terminal()
                print(terminal.clear())
                print(terminal.move(0,0))
            except:
                print(chr(27) + "[2J")

        if objtype == 'history':
            import readline
            for i in range(readline.get_current_history_length()):
                print(readline.get_history_item(i + 1))

        if objtype == 'help':
            import pydoc
            pydoc.pipepager(help_text, cmd='less -X -R -S') 

        if objtype == 'corpus':
            if not hasattr(obj, 'name'):
                print('Corpus not set. use "set <corpusname>".')
                return
            else:
                print(obj)
        
        elif objtype == 'python' or objtype == 'ipython':
            switch_to_ipython(args)

        elif objtype.startswith('jupyter') or objtype == 'notebook':
            switch_to_jupyter(args)

        elif objtype == 'gui':
            switch_to_gui(args)
        
        elif objtype in ['result', 'edited', 'totals',
                         'features', 'postags', 'wordclasses', 'series']:
            show_this(objtype)
        elif objtype == 'concordance':
            show_concordance(args)
        elif objtype == 'wordlists':
            show_this([objtype])
        elif objtype == 'wordlist':
            print(objs.wordlist)
        elif objtype.startswith('wordlist'):
            o, l = objtype.split('.', 1) if '.' in objtype else objtype.split(':', 1)
            print(getattr(objs.wordlists, l))
        elif objtype == 'query':
            show_this([objtype])
        else:
            pass

    def set_something(tokens):
        """
        Set the active corpus, a corpus filter, subcorpus structure, or option:

        :Examples:

           `set junglebook-parsed`
           `set decimal as 3`
           `set just topic as freedom|democracy`
           `set max_rows as 1000`
           `set papers as corpora`

        """
        if tokens and tokens[0].startswith('decimal'):
            objs._decimal = int(tokens[2])
            print('Decimal places set to %d.' % objs._decimal) 
            return

        if tokens and tokens[0] in ['show']:
            show = process_kwargs(['with'] + tokens).get('show', False)
            if not show:
                raise ValueError("Unreadable show value: %s" % ' '.join(tokens[2:]))
            objs._token_show_format = show
            print('Tokens will be displayed as: %s' % ', '.join(show))
            return

        if tokens and tokens[0] in ['max_cols', 'max_rows']:
            dim = 'rows' if tokens[0].endswith('rows') else 'columns'
    
            if tokens[-1] in ['off', 'all', 'false', 'False', 'None', 'none']:
                setattr(objs, tokens[0], None)
                print("Max %s turned off." % dim)
                return
            else:
                setattr(objs, tokens[0], int(tokens[-1]))
                print('Max %s set to %s.' % (dim, format(int(tokens[-1]), ',')))
                return

        # set subcorpora as attribute of corpus object ... is this ideal?
        if tokens and tokens[0].startswith('subcorp'):
            if tokens[-1] in ['false', 'none', 'normal', 'off',
                              'folder', 'folders', 'False', 'None']:
                tokens[-1] = False
            objs.symbolic = tokens[-1]
            #objs.corpus = Corpus(objs.corpus, subcorpora=tokens[-1], print_info=False)
            print('Set subcorpora to "%s".' % (tokens[-1]))
            return

        # setting skipping and just filters
        if tokens and tokens[0] in ['skip', 'just']:
            attr = tokens[0]
            # if the filter is already in the dict
            if isinstance(getattr(objs, tokens[0]), dict) and tokens[1] in getattr(objs, tokens[0]).keys():
                oldd = getattr(objs, tokens[0])
                # delete it
                if tokens[-1] in ['none', 'None', 'off', 'default']:
                    oldd.pop(tokens[1], None)
                    setattr(objs, tokens[0], oldd)
                # modify it
                else:
                    oldd[tokens[1]] = parse_pattern(tokens[-1])
                    setattr(objs, tokens[0], oldd)
            # delete the entire filter dict
            elif tokens[-1] in ['none', 'None', 'off', 'default']:
                setattr(objs, attr, False)
                print("Reset %s filter." % attr)
                return
            # if not in dict, add it
            metfeat = tokens[1]
            crit = tokens[-1]
            if crit.startswith('tag'):
                setattr(objs, attr, {'tags': parse_pattern(crit)})
            else:
                if isinstance(getattr(objs, attr, False), dict):
                    d = getattr(objs, attr)
                    d[metfeat] = parse_pattern(crit)
                    setattr(objs, attr, d)
                else:
                    setattr(objs, attr, {metfeat: parse_pattern(crit)})
            print("Current %s filter: %s" % (attr, getattr(objs, attr)))
            return

        if not check_in_project():
            print("Must be in project to set corpus.")
            return
        
        if not tokens:
            # todo: pick first one if only one
            show_this(['corpora'])
            selected = INPUTFUNC('Pick a corpus by name or number: ')
            selected = selected.strip()
            if not selected:
                return
            elif selected.isdigit():
                dirs = [x for x in os.listdir('data') \
                        if os.path.isdir(os.path.join('data', x))]
                set_something([dirs[int(selected)-1]])
                return
            else:
                set_something([selected])
                return

        path = tokens[0]
        loadsaved = len(tokens) > 1 and tokens[1].startswith('load')

        kwargs = process_kwargs(tokens, fixjust=True)
        if debug:
            print('KWARGS', kwargs)

        if os.path.exists(path) or os.path.exists(os.path.join('data', path)):
            objs.corpus = Corpus(path, **kwargs)
        else:
            dirs = [x for x in os.listdir('data') if os.path.isdir(os.path.join('data', x))]
            corpname = dirs[int(tokens[0])-1]
            set_something([corpname] + tokens[1:])


    def get_something(tokens):
        """
        Get a subcorpus or file of a corpus

        :Example:

        get file 1 from corpus

        """
        # if the user wants to start at a sentence
        start_pos = False
        six = next((i for i, w in enumerate(tokens) if w.startswith('sent')), -1) + 1
        if six:
            start_pos = int(tokens[six])
            tokens = [t for i, t in enumerate(tokens) if i != six and i != six-1]

        target_corpus = 'corpus'
        if len(tokens) > 2:
            target_corpus = tokens[-1]
        corpp = objs._get(target_corpus)[1]
        getwhat = 'files' if tokens[0] == 'file' else 'subcorpora'
        dlist = getattr(corpp, getwhat)
        try:
            ix = int(tokens[1]) - 1
        except:
            ix = tokens[1]
        ob = dlist[ix]
        if objs._interactive and hasattr(ob, 'document'):
            ndf = ob.document
            ndf.columns = ['Word', 'Lemma', 'POS', 'NER', 'Morphology', 'Governor', 'Function', 'Dependents', 'Co-reference']
            ndf.index.names = ['Sentence', 'Token']
            start_pos = next((i for i, l in enumerate(ndf.index.labels[0]) if l == start_pos), 0)
            show_table(ndf, objtype=False, start_pos=start_pos)
        objs.sampled = ob
        print('Sample created.')
        return

    def parse_search_related(search_related):
        """
        parse the capitalised tokens in
        'search corpus FOR GOVERNOR-LEMMA MATCHING XYZ AND
            LEMMA MATCHING .* showing ...'
        """
        search = {}
        exclude = {}   
        searchmode = 'all'
        cqlmode = False
        depgrepmode = False
        if search_related[0] != 'for':
            search_related.insert(0, 'for')
        for i, token in enumerate(search_related):
            if token in ['for', 'and', 'not', 'or']:
                if token == 'or':
                    searchmode = 'any'
                if search_related[i+1] == 'not':
                    continue
                if search_related[i+1] == 'features':
                    search = 'features'
                    continue
                if search_related[i+1] == 'postags':
                    search = 'postags'
                    continue
                if search_related[i+1] == 'wordclasses':
                    search = 'wordclasses'
                    continue
                k = search_related[i+1]
                if k == 'cql':
                    cqlmode = True
                    aquery = next((i for i in search_related[i+2:] \
                                  if i not in ['matching']), False)
                    if aquery:
                        search = {'c': aquery}
                        break
                if k == 'depgrep' or k == 'dependencies' or k == 'dependency':
                    depgrepmode = True
                    aquery = next((i for i in search_related[i+2:] \
                                  if i not in ['matching']), False)
                    if aquery:
                        search = {'d': aquery}
                        break      
                if k == 'trees' or k == 'tree' or k == 'tgrep':
                    aquery = next((i for i in search_related[i+2:] \
                                  if i not in ['matching']), False)
                    if aquery:
                        search = {'t': aquery}
                        break           
                k = process_long_key(k)
                v = search_related[i+3].strip("'")
                v = parse_pattern(v)
                if token == 'not':
                    exclude[k] = v
                else:
                    search[k] = v
        return search, exclude, searchmode, cqlmode, depgrepmode

    def process_long_key(srch):
        """
        turn governor-lemma into 'gl', etc.
        """
        
        transobjs = {v.lower(): k.replace(' ', '-') for k, v in transobjs.items()}
        transshow = {v.lower(): k.replace(' ', '-') for k, v in transshow.items()}
        showplurals = {k + 's': v for k, v in transshow.items()}
        objsplurals = {k + 's': v for k, v in transobjs.items()}
        
        transshow['distance'] = 'r'
        transshow['ngram'] = 'n'
        transshow['distances'] = 'r'
        transshow['ngrams'] = 'n'
        transshow['wordclass'] = 'x'
        transshow['wordclasses'] = 'x'
        transshow['count'] = 'c'

        transshow.update(showplurals)
        transobjs.update(objsplurals)

        ngram = srch.startswith('n')
        colls = srch.startswith('b')

        if ngram or colls:
            newsrch = srch.split('-', 1)[-1]
            if newsrch == srch:
                srch = 'nw' if ngram else 'bw'
            else:
                srch = newsrch

        srch = srch.lower()
        
        if '-' not in srch:
            if srch in transobjs:
                string = transobjs.get(srch) + 'w'
            elif srch in transshow or srch.startswith('t'):
                if not srch.startswith('t'):
                    string = 'm' + transshow.get(srch)
                else:
                    string = transshow.get(srch, 't')
            else:
                string = srch
        else:
            obj, show = srch.split('-', 1)
            string = '%s%s' % (transobjs.get(obj, obj), transshow.get(show, show))
        if ngram:
            return 'n' + string
        elif colls:
            return 'b' + string
        else:
            return string

    def parse_pattern(val):
        """
        Parse the token after 'matching'---that is, the search criteria
        """
        trans = {'true': True,
                 'false': False,
                 'on': True,
                 'off': False,
                 'none': None}

        # this means that if the query is a variable, the variable is returned
        # maybe this is not ideal behaviour.
        if val in objs.named.keys():
            return objs.named[val]

        if any(val.startswith(x) for x in ['role', 'process', 'wordlist']) \
            and any(x in [':', '.'] for x in val):
            lis, attrib = val.split('.', 1) if '.' in val else val.split(':', 1)
            customs = []
            from corpkit.dictionaries import roles, processes, wordlists
            mapped = {'roles': roles,
                      'processes': processes}

            if lis.startswith('wordlist'):
                lst = objs.wordlists.get(attrib)
            else:
                lst = getattr(mapped.get(lis), attrib)
            if lst:
                return lst
            else:
                print('Wordlist "%s" unrecognised.' % attrib)

        if val.isdigit():
            return int(val)
        elif val.startswith('[') and val.endswith(']'):
            val = val.lstrip('[').rstrip(']')
            if ', ' in val:
                return val.strip('"').strip("'").split(', ')
            elif ',' in val:
                return val.strip('"').strip("'").split(',')
            elif ' ' in val:
                return val.strip('"').strip("'").split()

        elif val.lower() in trans.keys():
            return trans.get(val.lower())
        # interpret columns
        elif all(i in ['i', 'c', 'f', 's', 'l', 'm', 'r'] for i in val.lower()) and len(val) <= 6:
            return [i for i in val.lower()]
        else:
            if val in dir(__builtins__) + ['any', 'all']:
                return val
            try:
                return eval(val)
            except (SyntaxError, NameError):
                return val

    def search_helper(text='search'):
        """
        Interactive mode for search, exclude or show
        """

        if text in ['search', 'exclude']:
            search_or_show = {}
        else:
            search_or_show = []
        while True:
            out = INPUTFUNC('\n    %s (words, lemma, pos, function ... ) > ' % text)
            out = out.lower()
            
            if not out:
                break
            if out.startswith('done'):
                break


            if out == 'cql':
                cql = INPUTFUNC('\n        CQL query > ')
                return cql.strip()
            if text == 'show':
                out = out.replace(', ', ' ').replace(',', ' ').replace('/', ' ')
                return out.split(' ')
                #search_or_show.append(out)
                #continue
            val = INPUTFUNC('\n        value (regex, wordlist) > ')
            if not val:
                continue
            if val.startswith('done'):
                break
            out = process_long_key(out)
            search_or_show[out] = parse_pattern(val)

        return search_or_show

    def process_kwargs(tokens, fixjust=False):
        """
        Turn the last part of a command into a dict of kwargs
        """
        from collections import defaultdict
        if 'with' in tokens:
            start = tokens.index('with')
            with_related = tokens[start+1:]
        else:
            with_related = []
        withs = defaultdict(list)
        skips = []

        for i, token in enumerate(with_related):
            if i in skips or token in ['and']:
                continue
            # this is used when making corpora with filters
            if fixjust:
                if token == 'skip':
                    pat = parse_pattern(with_related[i+3])
                    withs['skip'] = {with_related[i+1]: pat}
                elif token == 'just':
                    pat = parse_pattern(with_related[i+3])
                    withs['just'] = {with_related[i+1]: pat}
                skips.append(i+1)
                skips.append(i+2)
                skips.append(i+3)
                if token in ['skip', 'just']:
                    continue
            if token == 'not':
                withs[with_related[i+1].lower()] = False
                skips.append(i+1)
            elif '=' not in token:
                if len(with_related) >= i+2 and with_related[i+1] == 'as':
                    n = 2
                    val = with_related[i+n]
                    skips.append(i+1)
                    skips.append(i+2)
                    if token.lower() in ['columns', 'm', 'middle', 'show']:
                        parsed = process_long_key(val.strip(','))
                    else:
                        parsed = parse_pattern(val.rstrip(','))
                    withs[token.lower()].append(parsed)
                    while val.endswith(','):
                        n += 1
                        skips.append(i+n)
                        val = with_related[i+n]
                        if token.lower() in ['columns', 'm', 'middle', 'show']:
                            parsed = process_long_key(val.strip(','))
                        else:
                            parsed = parse_pattern(val.rstrip(','))
                        withs[token.lower()].append(parsed)
                else:
                    withs[token.lower()] = True
            elif '=' in token:
                k, v = token.lower().split('=', 1)
                v = parse_pattern(v)
                withs[k] = v

        out = {}
        for k, v in withs.items():
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            out[k] = v

        if debug:
            print('kwargs', out)
        return out

    def parse_show(tokens, word='showing'):
        if word in tokens:
            start = tokens.index(word)
            show_related = tokens[start+1:]
            end = show_related.index('with') if 'with' in show_related else False
            if end:
                show_related = show_related[:end]
        else:
            show_related = []
        show = []
        if show_related:
            for token in show_related:
                token = token.rstrip(',')
                if token == 'and':
                    continue
                token = process_long_key(token)
                show.append(token)
            objs._token_show_format = show
        else:
            show = ['w']
        return show

    def parse_search_args(tokens):
        """
        Put all search arguments together---search, exclude, show, and kwargs
        """
        tokens = tokens[1:]
        
        # interactive mode
        if not tokens:
            search = search_helper(text='search')
            exclude = search_helper(text='exclude')
            show = search_helper(text='show')
            show = [process_long_key(i) for i in show]
            kwargs = {'search': search, 'show': show, 'exclude': exclude,
                      'cql': isinstance(search, str)}
            return kwargs

        search_related = []
        for token in tokens:
            search_related.append(token)
            if token in [',', 'showing', 'with', 'excluding']:
                break

        if 'excluding' in tokens:
            start = tokens.index('excluding')
            ex_related = tokens[start+1:]
            end = ex_related.index('showing') if 'showing' in ex_related else False
            if end is False:
                end = ex_related.index('with') if 'with' in ex_related else False
            if end:
                ex_related = ex_related[:end]
        else:
            ex_related = []

        show = parse_show(tokens)

        if 'with' in tokens:
            start = tokens.index('with')
            with_related = tokens[start+1:]
        else:
            with_related = []

        search, exclude, searchmode, cqlmode, depgrepmode = parse_search_related(search_related)
        if not exclude and ex_related:
            exclude, _, _, _, _, _ = parse_search_related(ex_related)

        withs = process_kwargs(tokens)

        kwargs = {'search': search, 'exclude': exclude, 
                  'show': show, 'searchmode': searchmode}
        kwargs.update(withs)
        return kwargs

    def search_corpus(tokens):
        """
        Search a corpus for lexicogrammatical features. You are limited only by your imagination.
        
        :Syntax:

        search corpus for [object matching pattern]* showing [things to show]* with [extra options]*
         
        The asterisk marked parts of the query can be recursive and negated

        :Examples:

           > search corpus for cql matching '[word="test"]' showing word and lemma
           > search corpus for governor-function matching roles:process with coref
           > search corpus for trees matching "/NN.?/ >># NP" 
           > search corpus for words matching "^[abcde]" with preserve_case and case_sensitive
        """

        corpp = objs._get(tokens[0])[1]

        if corpp is None or corpp is False:
            print('Corpus not set. use "set <corpusname>".')
            return

        kwargs = parse_search_args(tokens)
        
        kwargs['just'] = objs.just
        kwargs['skip'] = objs.skip

        if debug:
            print(kwargs)

        sch = kwargs.get('search', False)
        if sch in ['features', 'postags', 'wordclasses']:
            objs.result = getattr(corpp, sch)
            try:
                objs.totals = getattr(corpp, sch).sum(axis=1)
            except:
                objs.totals = None
            #if objs._interactive:
            #    show_this([sch])
        else:
            objs.result = corpp.interrogate(**kwargs)
            if objs.result is not None:
                objs.totals = objs.result.totals
        # this should be done for pos and wordclasses too
        print('')

        if not isinstance(objs.result, (Results, pd.DataFrame, pd.Series)):
            return
        objs.previous = objs.result
        objs.query = getattr(objs.result, 'query', None)
        objs._old_searches.append(objs.result)
        objs.edited = False
        show_result(objs.result, [], **kwargs)
        return

    def show_result(to_show, tokens, **kwargs):
        kwargs = process_kwargs(tokens)
        subcorpora = kwargs.pop('subcorpora', 'default')
        show = kwargs.pop('columns', False)
        if not show:
            show = objs._token_show_format
        else:
            objs._token_show_format = show
        data = to_show.table(subcorpora=subcorpora, show=show, **kwargs)
        show_table(data)
        objs._last_shown = 'table'
        return

    def show_this(tokens):
        """
        Show any object in a human-readable form
        """
        if tokens[0] == 'edited' or objs._get(tokens[0])[0] == 'edited':
            gotten = objs._get(tokens[0])[1]
            if tokens[1] == 'result':
                show_result(gotten, tokens)
            elif tokens[1] == 'concordance':
                show_concordance(tokens, conc_obj=gotten)
            return
        if tokens[0] == 'result' or objs._get(tokens[0])[0] == 'result':
            gotten = objs._get(tokens[0])[1]
            show_result(gotten, tokens[1:])
            return
        if tokens[0] == 'concordance' or objs._get(tokens[0])[0] == 'concordance':
            show_concordance(tokens[1:])
            return
        if tokens[0].startswith('file'):
            get_something[tokens]
            return
        if tokens[0] == 'corpora':
            dirs = [x for x in os.listdir('data') if \
                     os.path.isdir(os.path.join('data', x))]
            dirs = ['\t%d: %s' % (i, x) for i, x in enumerate(dirs, start=1)]
            print ('\n'.join(dirs))
        elif tokens[0].startswith('store'):
            for k, v in objs.stored.items():
                print(k, v)
        elif tokens[0].startswith('filter'):
            print('Skip:', getattr(objs, 'skip', 'none'))
            print('Just:', getattr(objs, 'just', 'none'))
        elif tokens[0].startswith('subcorp'):
            print('Symbolic structure:', getattr(objs, 'symbolic', 'none'))
        elif tokens[0].startswith('wordlists'):
            if '.' in tokens[0] or ':' in tokens[0]:
                if ':' in tokens[0]:
                    _, attr = tokens[0].split(':')
                else:
                    _, attr = tokens[0].split('.')
                print(objs.wordlists.get(attr))
            else:
                for k, v in sorted(objs.wordlists.items()):
                    showv = str(v[:5])
                    if len(v) > 5:
                        showv = showv.rstrip('] ') + ' ... ]'
                    print('"%s": %s' % (k, showv))

        elif tokens[0] == 'saved':
            ss = [i for i in os.listdir('saved_interrogations') \
                   if not i.startswith('.')]
            print ('\t' + '\n\t'.join(ss))
        elif tokens[0] == 'query':
            for k, v in sorted(objs.query.items()):
                print('%s: %s' % (str(k), str(v)))
        elif tokens[0] == 'figure':
            if hasattr(objs, 'figure') and objs.figure:
                objs.figure.show()
            else:
                print('Nothing here yet.')
        elif tokens[0] in ['features', 'wordclasses', 'postags']:
            show_table(getattr(objs.corpus, tokens[0]))
        elif objs._get(tokens[0]):
            single_command_print(tokens)
        else:
            print("No information about: %s" % tokens[0])

    def get_info(tokens):
        pass

    def edit_interrogation(tokens):
        """
        Edit an interrogation or concordance

        :Example:

           `edit result by skippings subcorpora matching [1,2,3] with keep_top as 5`

        """

        thing_to_edit = get_thing_to_edit(tokens[0])

        trans = {'skipping': 'skip',
                 'keeping':  'just',
                 'merging':  'merge',
                 'spanning': 'span'}

        recog = ['not', 'matching', 'result', 'entry', 'entries',
                 'results', 'subcorpus', 'subcorpora', 'edited']

        ## skip, keep, merge
        by_related = []
        if 'by' in tokens:
            start = tokens.index('by')
            by_related = tokens[start+1:]

        if not by_related:
            inter = interactive_edit(tokens)

        kwargs = {}
        skips = []
        for i, token in enumerate(by_related):
            if i in skips:
                continue
            if token in trans:
                funcname = trans.get(token)
                k = by_related[i+1]
                v = next((x for x in by_related[i+2:] if x not in recog), False)
                if not v:
                    print('value not found.')
                    return
                v = parse_pattern(v)
                # edit result by merging subcorpora matching chapter[123] as first
                if token == 'merging':
                    newname = next(tokens[i+1] for i, t in enumerate(tokens) if t == 'as')
                    v = {newname: v}
                print(thing_to_edit, funcname, k, v)
                thing_to_edit = getattr(thing_to_edit, funcname)({k: v})
        
        objs.edited = thing_to_edit
        if objs._last_shown == 'conc':
            show_concordance([], objs.edited)

        elif objs._last_shown == 'table':
            show_this(['edited'])

    def run_command(tokens):
        """
        Run command and send output to objs class
        """

        command = get_command.get(tokens[0], unrecognised)        
        out = command(tokens[1:])


    def add_colour_to_conc_df(conc):
        """
        Exporting conc lines needs to preserve colouring
        """
        colourdict = objs._conc_colours[len(objs._old_searches)-1]
        fores = []
        backs = []
        stys = [] 
        for index in list(conc.index):
            line = colourdict.get(str(index))
            if not line:
                fores.append('')
                backs.append('')
                stys.append('')
            else:
                fores.append(line.get('Fore', ''))
                backs.append(line.get('Back', ''))
                stys.append(line.get('Style', ''))

        if any(i != '' for i in fores):
            conc['Foreground'] = fores
        if any(i != '' for i in backs):
            conc['Background'] = backs
        if any(i != '' for i in stys):
            conc['Style'] = stys
        return conc
        
    def export_result(tokens):
        """
        Send a result, edited result or concordance to file

        :Example:

           `export result as csv to out.csv`
           `export concordance as latex to concs.tex`

        """
        import os
        obj = objs._get(tokens[0])[1]
        
        if tokens[0].startswith('conc'):
            obj = add_colour_to_conc_df(obj.copy())

        if tokens[0] in ['result', 'edited']:
            obj = getattr(obj, 'results', obj)
        
        if len(tokens) == 1:
            print(obj.to_string())
            return
        tokens = tokens[1:]

        if 'as' in tokens:
            formt = tokens[tokens.index('as') + 1][0]
            tokens = tokens[tokens.index('as') + 2:]
        else:
            formt = 'c'

        if tokens:
            buf = tokens[-1]
        else:
            buf = None
        
        if buf == formt:
            buf = None
        
        if os.pathsep not in buf:
            buf = os.path.join('exported', buf)
        if formt == 'c':
            obj.to_csv(buf, sep='\t')
        elif formt == 's':
            obj.to_string(buf)
        elif formt == 'l':
            obj.to_latex(buf)

        if buf:
            if os.path.isfile(buf):
                print('Saved to: %s' % buf)
            else:
                print('Problem exporting file.')

    def interactive_edit(tokens):
        print('Not done yet')
        pass

    def get_thing_to_edit(token):
        thing = objs._get(token)[1]
        if thing is None:
            thing = objs.result
        return thing

    def sort_something(tokens):
        """
        Sort a result or concordance line
        """
        #todo: ascending, l1, etc
        thing_to_edit = get_thing_to_edit(tokens[0])
        std = thing_to_edit.sort_values(by=tokens[-1])
        setattr(objs, tokens[0], std)
        if objs._last_shown == 'conc':
            show_concordance([], conc_obj=std)
        else:
            show_table(std)

    def old_sort_something(tokens):
        """
        Sort a result or concordance line
        """

        thing_to_edit = get_thing_to_edit(tokens[0])

        recog = ['by', 'with', 'from']

        val = next((x for x in tokens[1:] if x not in recog), 'total')

        if not isinstance(thing_to_edit, Concordance):
            sortedd = thing_to_edit.edit(sort_by=val)
            if sortedd == 'linregress':
                raise ValueError("scipy needs to be installed for linear regression sorting.")
            objs.edited = sortedd
            objs.totals = objs.edited.totals
            return objs.edited
        else:
            if val.startswith('i'):
                sorted_lines = thing_to_edit.sort_index()
            else:
                if val[0] in ['l', 'm', 'r']:
                    
                    l_or_r = thing_to_edit[val[0]]
                    
                    if len(val) == 1:
                        val = val + '1'

                    ind = int(val[1:])

                    val = val[0]

                    if val == 'l':
                        ind = -ind
                    else:
                        ind = ind - 1

                    import numpy as np

                    # bad arg parsing here!
                    if 'slashsplit' in tokens:
                        splitter = '/'
                    else:
                        splitter = ' '

                    to_sort_on = l_or_r.str.split(splitter).tolist()
                    if val == 'l':
                        # todo: this is broken on l2,l3 etc
                        to_sort_on = [i[ind].lower() if i and len(i) >= abs(ind) \
                                  else np.nan for i in to_sort_on]
                    else:
                        to_sort_on = [i[ind].lower() if i and len(i) > abs(ind) \
                                  else np.nan for i in to_sort_on]
                    thing_to_edit['x'] = to_sort_on
                    val = 'x'

                elif val in ['scheme', 'color', 'colour']:
                    val = 'x'
                    num_col = objs._conc_colours[len(objs._old_searches)-1]
                    series = []
                    # todo: fix this!
                    for i in range(len(thing_to_edit)):
                        bit = num_col.get(str(i), 'zzzzz')
                        if isinstance(bit, dict):
                            bit = bit.get('Fore', bit.get('Back', 'zzzzz'))
                        series.append(bit)
                    thing_to_edit['x'] = series

                sorted_lines = thing_to_edit.sort_values(val, axis=0, na_position='last')
            
            if val == 'x':
                sorted_lines = sorted_lines.drop('x', axis=1)
            
            objs.concordance = Concordance(sorted_lines)

            # do not add new entry to old concs for sorting :)
            objs._old_searches[-1] = objs.concordance
            if objs._interactive:
                single_command_print('concordance')

    def plot_result(tokens):
        """
        Visualise an interrogation using matplotlib
        """
        
        import matplotlib.pyplot as plt
        kinds = ['line', 'heatmap', 'bar', 'barh', 'pie', 'area']
        kind = next((x for x in tokens if x in kinds), 'line')
        kwargs = process_kwargs(tokens)
        kwargs['tex'] = kwargs.get('tex', False)
        title = kwargs.pop('title', False)
        objs.figure = objs._get(tokens[0])[1].visualise(title=title, kind=kind, **kwargs)
        objs.figure.show()
        return objs.figure

    def asciiplot_result(tokens):
        """
        Visualise an interrogation with a simple ascii line chart
        """
        obj, attr = tokens[0].split(':', 1) if ':' in tokens[0] else tokens[0].split('.', 1)
        to_plot = objs._get(obj)[1]
        # if it said 'asciiplot result.this on axis 1', turn it into
        # asciiplot result.this with axis as 1

        if 'on' in tokens and not 'with' in tokens:
            tokens[tokens.index('on')] = 'with'
            if tokens[tokens.index('with')+1] == 'axis':
                if tokens[tokens.index('with')+2] in [0, 1]:
                    tokens.insert(tokens.index('with')+2, 'as')

        kwargs = process_kwargs(tokens)
        to_plot.asciiplot(attr, **kwargs)

    def calculate_result(tokens):
        """
        Get relative frequencies, combine results, do keywording

        :Syntax:

        calculate <result>/<edited> as <operation> of <denominator>

        :Examples:

           > calculate result as percentage of self
           > calculate edited as percentage of features.clauses
           > calculate result as percentage of stored.myname

        """
        # todo: use real syntax for keyness
        if 'k' in tokens or 'keyness' in tokens:
            operation = 'k'
        else:
            operation = False

        dd = {'percentage': '%',
              'key': 'k',
              'keyness': 'k'}

        calcs = ['k', '%', '+', '/', '-', '*', 'percentage', 'keyness']
        operation = next((i for i in tokens if any(i.startswith(x) for x in calcs)), operation)
        #todo: results!
        if not operation:
            if tokens[-1].startswith('conc'):
                res = objs.concordance.calculate()
                objs.result = res.results
                objs.totals = res.totals
                if objs._interactive:
                    show_this(['result'])
                return
            else:
                print('Bad operation.')
                return
        objtype, denominator = objs._get(tokens[-1])
        
        if tokens[-1] == 'self':
            denominator = 'self'

        operation = dd.get(operation, operation)

        the_obj = objs._get(tokens[0])[1]
        if not the_obj:
            the_obj = objs._get(tokens[-1])[1]

        objs.edited = the_obj.edit(operation, denominator)
        if hasattr(objs.edited, 'totals'):
            objs.totals = objs.edited.totals
        #print('\nedited:\n\n', objs.edited.results, '\n')
        return objs.edited

    def tokenise_corpus(tokens):
        """
        Tokenise an unparsed corpus

        :Example:

           `parse corpus with speaker_segmentation and metadata and multiprocess as 2`

        """
        typ, to_parse = objs._get(tokens[0])
        if typ != 'corpus':
            print('Command not understood. Use "set <corpusname>" and "parse corpus"')
        if not to_parse:
            print('Corpus not set. use "set <corpusname>" on an unparsed corpus.')
            return

        if to_parse.datatype != 'plaintext':
            print('Corpus is not plain text.')
            return

        kwargs = process_kwargs(tokens)
        parsed = to_parse.tokenise(**kwargs)
        if parsed:
            setattr(objs, 'corpus', parsed)
        return

    def parse_corpus(tokens):
        """
        Parse an unparsed corpus

        :Example:

           `parse corpus with speaker_segmentation and metadata and multiprocess as 2`

        """
        typ, to_parse = objs._get(tokens[0])
        if typ != 'corpus':
            print('Command not understood. Use "set <corpusname>" and "parse corpus"')
        if not to_parse:
            print('Corpus not set. use "set <corpusname>" on an unparsed corpus.')
            return

        if to_parse.datatype != 'plaintext':
            print('Corpus is not plain text.')
            return

        kwargs = process_kwargs(tokens)
        parsed = to_parse.parse(**kwargs)
        if parsed:
            setattr(objs, 'corpus', parsed)
        return

    def fetch_this(tokens, unbound=False):
        """
        Get something from storage

        :Example:

           `fetch my_result as result`
        """

        
        from_wl = False
        to_fetch = objs.stored.get(tokens[0], False)

        if to_fetch is False:
            to_fetch = objs.wordlists.get(tokens[0], False)
            from_wl = True
            if to_fetch is False:
                print('Not in store or wordlists: %s' % tokens[0])
                return

        if unbound:
            return to_fetch

        if from_wl:
            objs.wordlist = to_fetch
            showv = to_fetch[:5]
            if len(to_fetch) > 5:
                showv = str(showv).rstrip('] ') + ' ... ]'
            print('%s (%s) fetched as wordlist.' % (repr(tokens[0]), showv))
            return

        if len(tokens) < 3:
            if isinstance(to_fetch, Corpus):
                weneed = 'corpus'
            elif isinstance(to_fetch, Results):
                if hasattr(to_fetch, 'denominator'):
                    weneed = 'edited'
                else:
                    weneed = 'result'
            elif isinstance(to_fetch, Concordance):
                weneed = 'concordance'
        else:
            weneed = tokens[2]

        if weneed == 'corpus':
            objs.corpus = to_fetch
        elif weneed.startswith('conc'):
            objs.concordance = to_fetch
        elif weneed == 'result':
            objs.result = to_fetch
        elif weneed == 'edited':
            objs.edited = to_fetch

        print('%s fetched as %s.' % (repr(to_fetch), weneed))

    def save_this(tokens, passedin=False):
        """
        Save a result or concordance

        :Example:

           `save result as 'non_pronoun_actors'`
        """
        if passedin:
            to_save = passedin
        else:
            to_save = objs._get(tokens[0])[1]

        if to_save == 'store' and not passedin:
            for k, v in objs.stored.items():
                save_this(['as', k], passedin=v)

        if tokens[0] == 'figure' or hasattr(to_save, 'savefig'):
            tokens[-1] = os.path.join('images', tokens[-1])
            to_save.savefig(tokens[-1])
        else:
            to_save.save(tokens[-1])


    def load_this(tokens):
        """
        Load data from file, including corpus indexing
        """
        from corpkit.other import load
        if tokens[-1] == 'result':
            objs.result = load(tokens[0])
        #if tokens[-1] == 'concordance':
        #    objs.concordance = load(tokens[0])
        if tokens[-1] == 'edited':
            objs.edited = load(tokens[0])
        if tokens[0] == 'corpus':
            kwargs = process_kwargs(tokens)
            objs.corpus = objs.corpus.load(**kwargs)
        if 'all' in tokens:
            raise NotImplementedError

    def interactive_listmaker():
        done_words = []
        text = 'Enter words separated by spaces, or one per line. (Leave the line blank to end)\n\n\t> '
        while True:
            res = INPUTFUNC(text)
            text = '\t> '
            if res:
                if ',' in res:
                    words = [i.strip(', ') for i in res.split()]
                    for w in words:
                        done_words.append(w)
                elif ' ' in res.strip():
                    words = res.split()
                    for w in words:
                        done_words.append(w)
                else:
                    done_words.append(res.strip())
            else:                    
                return done_words
    
    def new_thing(tokens):
        """
        Start a new project with a name of your choice, then move into it
        """
        if tokens[0] == 'project':
            from corpkit.other import new_project
            new_project(tokens[-1])
            os.chdir(tokens[-1])
        if tokens[0] == 'wordlist':
            the_name = next((tokens[i+1] for i, t in enumerate(tokens) if t in ['called', 'named']), None)
            if not the_name:
                print('Syntax: new wordlist named <name>.')
                return
            if objs.wordlists.get(the_name):
                print('"%s" already exists in wordlists.' % the_name)
                return
            filename = next((tokens[i+1] for i, t in enumerate(tokens) if t in ['from']), None)
            if filename:
                with open(filename, 'r') as fo:
                    words = [i.strip() for i in fo.read().splitlines() if i]
            else:
                words = interactive_listmaker()
            if words:
                objs.wordlists[the_name] = words
                objs.wordlist = words
                print('Wordlist "%s" stored.' % the_name)

    def get_matching_indices(tokens):
        """
        Find concordance indices matching some criteria in tokens

        This can be:

            - an int as index: "20"
            - a pseudo index: "5-10"
            - a column and regex: "l matching 'regex'"
            - a colour name
            - 'all'

        :returns: a `set` of matching indices

        """
        # what's missing from this list?
        # hard coding in case user doesn't have colorama
        colours = ['red', 'yellow', 'magenta', 'lightmagenta_ex', 'black',
                   'white', 'lightcyan_ex', 'reset', 'green', 'lightyellow_ex',
                   'lightblack_ex', 'lightwhite_ex', 'blue', 'lightblue_ex',
                   'lightgreen_ex', 'cyan', 'lightred_ex']
        cols = []
        token = tokens[0]

        # for something like del red
        if token in colours:
            if tokens[-1].lower() == 'back':
                sty = 'Back'
            elif tokens[-1].lower() in ['dim', 'bright', 'normal', 'reset']:
                sty = 'Style'
            else:
                sty = 'Fore'
            colourdict = objs._conc_colours[len(objs._old_searches)-1]
            return set([k for k, v in colourdict.items() if v.get(sty) == token])  
            
        # annotate range of tokens
        if token == 'all':
            return [str(i) for i in list(objs.concordance.index)]

        elif '-' in token:
            first, last = token.split('-', 1)
            if not first:
                first = 0
            if not last:
                last = len(objs.concordance.index)
            for n in range(int(first), int(last)+1):
                cols.append(str(n))
        # get by index/indices
        elif token.isdigit():
            cols = [i for i in tokens if i.isdigit()]
        else:
            # regex match only what's shown in the window
            window = objs._conc_kwargs.get('window', 35)
            if token in list(objs.concordance.columns) \
                and token not in ['l', 'm', 'r']:
                token_bits = [token]
            else:
                token_bits = list(token)
            slic = slice(None, None)
            for bit in token_bits:
                if bit.lower() == 'm':
                    slic = slice(None, None)
                elif bit.lower() == 'l':
                    slic = slice(-window, None)
                elif bit.lower() == 'r':
                    slic = slice(None, window)
                # get slice for left window
                mx = max(objs.concordance[bit.lower()].str.len()) \
                         if bit.lower() == 'l' else 0
                # get the regex criteria
                if 'matching' in tokens:
                    rgx = tokens[tokens.index('matching') + 1]
                else:
                    rgx = tokens[1]
                rgx = parse_pattern(rgx)

                pol = not 'not' in tokens
                
                # get the window size of context, and reduce to just windows
                if isinstance(rgx, list):
                    trues = objs.concordance[bit].str.rjust(mx).str[slic].isin(rgx)
                else:
                    trues = objs.concordance[bit].str.rjust(mx).str[slic].str.contains(rgx)
                
                if pol:
                    mtch = objs.concordance[trues]
                else:
                    mtch = objs.concordance[~trues]
                matches = list(mtch.index)
                for ind in matches:
                    cols.append(str(ind))

        return set(cols)

    def parse_anno_with(tokens):
        """
        Decide what the text is for an annotation
        """
        if tokens[0] == 'tag':
            return tokens[-1]
        elif tokens[0] == 'field':
            tokens = tokens[1:]
            nx = next((i for i, w in enumerate(tokens) if w != 'as'), 0)
            return {tokens[nx]: tokens[-1]}

    def unannotate_corpus(tokens):
        """
        Remove annotations from a corpus

        :Example:

           `unannotate character field`
           `unannotate friend tag`
        """
        to_remove = tokens[0]
        from corpkit.annotate import annotator
        # right now, you can't delete just a value...
        if tokens[-1] == 'field':
            to_remove = {to_remove: r'.*'}
        if to_remove == 'all' and tokens[-1].startswith('tag'):
            to_remove = {'tags': r'.*'}
        #elif tokens[-1] == 'tag':

        annotator(df_or_corpus=objs.corpus,
                  annotation=to_remove,
                  dry_run=not objs._annotation_unlocked,
                  deletemode=True)
        if not objs._annotation_unlocked:
            print("\nIf you really want to delete these annotations from the corpus, " \
                  "do `toggle annotation` and run the previous command again.\n")
        else:
            print('Deleted %s annotations.' % tokens[0])

    def annotate_corpus(tokens):
        """
        Add annotations to the corpus

        :Example:

           `annotate m matching 'ing$' with tag as 'mytag'`
           `annotate m matching 'ing$' with field as 'person' and value as 'daisy'`
        """

        cols = get_matching_indices(tokens)
        from corpkit.annotate import annotator
        df = objs.concordance.ix[[int(i) for i in list(cols)]]

        if 'with' in tokens:
            start = tokens.index('with')
            with_related = tokens[start+1:]
        else:
            with_related = []
        annotation = parse_anno_with(with_related)
        
        annotator(df, annotation, dry_run=not objs._annotation_unlocked)
        if not objs._annotation_unlocked:
            print("\nWhen you're ready to actually add annotations to the files, " \
                  "do `toggle annotation` and run the previous command again.\n")
        else:
            print('Corpus annotated (%d additions).' % len(df.index))

    def annotate_conc(tokens):
        """
        Annotate concordance lines matching criteria with a colour or style

        :Example:

           `mark m matching 'ing$' red`
        """
        from colorama import Fore, Back, Style, init
        init(autoreset=True)
        cols = get_matching_indices(tokens)
        color = tokens[-1]
        if color in ['dim', 'normal', 'bright']:
            sty = 'Style'
        elif 'back' in tokens or 'background' in tokens:
            sty = 'Back'
        else:
            sty = 'Fore'
        #if tokens[-2].lower() in ['back', 'dim', 'fore', 'normal', 'bright', 'background', 'foreground']:
        #    sty = tokens[-2].title().replace('ground', '')

        for line in cols:
            line = int(line)
            if not line in list(objs.concordance.index):
                continue
            # if there is already info for this line number, add present info
            if objs._conc_colours[len(objs._old_searches)-1].get(line):
                objs._conc_colours[len(objs._old_searches)-1][line][sty] = color
            else:
                objs._conc_colours[len(objs._old_searches)-1][line] = {}
                objs._conc_colours[len(objs._old_searches)-1][line][sty] = color

        single_command_print(['concordance'] + tokens)

    def add_corpus(tokens):
        """
        Copy a folder to the ./data directory of a project

        :Example:

           `add '../../data'`
        """
        import shutil
        the_path = os.path.expanduser(tokens[-1])
        outf = os.path.join(os.getcwd(), 'data', os.path.basename(the_path))
        # if we're using docker things get tricky
        if objs._docker:
            # not working yet
            import subprocess
            from docker import Client
            cli = Client()
            idx = str(subprocess.check_output(["cat", "/etc/hostname"])).strip('\n').strip()
            outf = ':'.join([idx, outf])
            os.makedirs(outf)
            os.system("docker cp %s/ %s" % (the_path, outf))
            #cli.copy(the_path, outf)
            print('%s added to %s.' % (tokens[-1], outf))
            return
        shutil.copytree(the_path, outf)
        print('%s added to %s.' % (tokens[-1], outf))

    def del_conc(tokens):
        """
        Delete concordance lines matching criteria

        :Example:

           `del m matching 'ing$'`
        """
        cols = get_matching_indices(tokens)
        cols = [int(i) for i in cols]
        objs.concordance = Concordance(objs.concordance.drop(cols, axis=0))
        return objs.concordance

    def keep_conc(tokens):
        """
        Keep concordance lines matching criteria

        :Example:

           `keep m matching 'ing$'`
        """
        cols = get_matching_indices(tokens)
        cols = [int(i) for i in cols]
        objs.concordance = Concordance(objs.concordance.loc[cols])
        return objs.concordance

    def store_this(tokens):
        """
        Send a result into storage

        :Example:

           `store result as 'processes'`

        To view the contents of the store, do `show store`.

        """

        to_store = objs._get(tokens[0])[1]

        #if not to_store:
        #    print('Not storable:' % tokens[0])
        #    return

        if tokens[1] == 'as':
            name = tokens[2]
        else:
            count = 0
            while str(count) in objs.stored.keys():
                count += 1
            name = str(count)
        if name in objs.stored.keys():
            cont = INPUTFUNC('%s already in store. Replace it? (y/n) ')
            if cont.lower().startswith('n'):
                return
        objs.stored[name] = to_store
        print('Stored: %s' % name)

    def toggle_this(tokens):
        """
        Toggle a specified option

        Currently available:

        - toggle conc (does concordancing when searching)
        - toggle interactive (shows results and concordances after running)
        - toggle annotation (allows the user to annotate the real corpus)
        - toggle comma (shows thousands comma in results)

        """
        if tokens[0].startswith('interactive'):
            objs._interactive = not objs._interactive
            s = 'on' if objs._interactive else 'off'
            print('Auto showing of results and concordances turned %s.' % s)
        if tokens[0].startswith('anno'):
            objs._annotation_unlocked = not objs._annotation_unlocked
            s = 'on' if objs._annotation_unlocked else 'off'
            print('Annotation mode %s.' % s)
        if tokens[0].startswith('comma'):
            objs._comma = not objs._comma
            s = 'on' if objs._comma else 'off'
            print('Thousand separator in results turned %s.' % s)

    def remove_something(tokens):
        if len(tokens) == 1:
            objs.named.pop(tokens[0])
        else:
            frm = getattr(objs, tokens[-1])
            frm.pop(tokens[0])
        print('Forgot %s.' % tokens[0])

    def name_something(tokens):
        """
        Basically, make a variable. In reality,
        it is a key-value pair in objs.named

        """
        # get the object if it exists somewhere
        originally_was, thing = objs._get(tokens[0])

        if thing is None or thing is False:
            thing = tokens[0]
            if thing == 'py':
                thing = eval(tokens[1])
                originally_was = 'eval'
                tokens = tokens[1:]
            else:
                originally_was = 'string'
            #print('Nothing stored in %s to name.' % tokens[0])
            #return
        
        # this should just be objects!
        if tokens[0] in objs._protected:
            originally_was = tokens[0]
        
        from corpkit.process import makesafe
        name = makesafe(tokens[-1])
        if name in objs._protected + list(get_command.keys()):
            print('The name "%s" is protected, sorry.' % name)
        else:
            objs.named[name] = (originally_was, thing)
            print('%s named "%s".' % (tokens[0], name))

    def sample_something(tokens):
        """
        Make a sample from a corpus
        
        :Example:

           sample 2 subcorpora of corpus
           sample 100 files of corpus 
        """
        trans = {'s': 'subcorpora', 'f': 'files'}
        originally_was, thing = objs._get(tokens[-1])
        if '.' in tokens[0]:
            n = float(tokens[0])
        else:
            n = int(tokens[0])
        level = tokens[1].lower()[0]
        samp = thing.sample(n, level)
        objs.sampled = samp
        #todo: proper printing
        names = [i.name for i in getattr(objs.sampled, trans[level])]
        form = ', '.join(names[:3])
        if len(names) > 3:
            form += ' ...'
        print('Sample created: %d %s from %s --- %s' % (n, trans[level],
                                                        thing.name, form))

    def ch_dir(tokens):
        """
        Change directory

        :Example:

           `cd essays`

        """
        import os
        os.chdir(tokens[0])
        print(os.getcwd())
        get_prompt()

    def ls_dir(tokens):
        """
        List directory contents
        
        :Example:

           `ls data`

        """
        import os
        nonhidden = [i for i in os.listdir(tokens[0]) if not i.startswith('.')]
        print('\n'.join(nonhidden))

    get_command = {'set': set_something,
                   'get': get_something,
                   'show': show_this,
                   'search': search_corpus,
                   'info': get_info,
                   'parse': parse_corpus,
                   'export': export_result,
                   'mark': annotate_conc,
                   'annotate': annotate_corpus,
                   'unannotate': unannotate_corpus,
                   'del': del_conc,
                   'just': keep_conc,
                   'sort': sort_something,
                   'sample': sample_something,
                   'toggle': toggle_this,
                   'edit': edit_interrogation,
                   'tokenise': tokenise_corpus,
                   'tokenize': tokenise_corpus,
                   'ls': ls_dir,
                   'cd': ch_dir,
                   'plot': plot_result,
                   'asciiplot': asciiplot_result,
                   'help': helper,
                   'store': store_this,
                   'new': new_thing,
                   'fetch': fetch_this,
                   'call': name_something,
                   'remove': remove_something,
                   'save': save_this,
                   'load': load_this,
                   'calculate': calculate_result,
                   'add': add_corpus}

    objmap = {search_corpus: 'result',
              edit_interrogation: 'edited',
              calculate_result: 'edited',
              sort_something: 'edited',
              plot_result: 'figure',
              set_something: 'corpus',
              load_this: 'result'}

    def unrecognised(*args, **kwargs):
        print('unrecognised!')

    import shlex

    if debug:
        try:
            objs.corpus = Corpus('jb-parsed')
        except:
            pass

    def get_prompt(backslashed=False):
        """
        Create the prompt, based on being in project etc.

        :param backslashed: is when there is a line continuation
        """
        folder = os.path.basename(os.getcwd())
        proj_dirs = ['data', 'saved_interrogations', 'exported']
        objs._in_a_project = check_in_project()
        end = '*' if not objs._in_a_project else ''
        name = getattr(objs.corpus, 'name', 'no-corpus')
        txt = 'corpkit@%s%s:%s> ' % (folder, end, name)
        if not backslashed:
            return txt
        else:
            return '... '.rjust(len(txt))

    def nest_on_semicolon(tokens):
        """
        Take a tokenised command and make a nested list,
        which accounts for ';' breaks
        """
        if ';' not in tokens:
            return [tokens]
        nested = []
        while tokens:
            s_ix = next((i for i, x in enumerate(tokens) if x == ';'), len(tokens))
            nested.append(tokens[:s_ix])
            tokens = tokens[s_ix+1:]
        return nested

    if not fromscript and not python_c_mode:
        print(allig)

    if not check_in_project():
        print("\nWARNING: You aren't in a project yet. "\
              "Use 'new project named <name>' to make one and enter it.\n"\
              "Alternatively, you can `cd` into an existing project now.\n")

    def do_bash(output):
        """
        Run text as shell command
        """
        import os
        os.system(output.lstrip('! '))

    # backslashed allows line breaks with backslashes ala python.
    # it's a bit of a hack, but seems to work pretty well

    backslashed = ''

    if fromscript:
        commands = read_script(fromscript)
        objs._interactive = False

    if python_c_mode:
        objs._interactive = False

    if loadcurrent:
        load_this(['all'])

    # the main loop, with exception handling
    while True:
        try:
            if not fromscript and not python_c_mode and not profile:
                output = INPUTFUNC(get_prompt(backslashed))
            
            elif fromscript:
                if not commands:
                    break
                output = commands.pop()
            
            elif python_c_mode:
                output = python_c_mode

            elif profile:
                output = 'quit'

            # terminate
            if output.lower() in ['exit', 'quit', 'exit()', 'quit()']:
                break

            # do nothing
            if not output:
                output = True
                continue
            
            # append line to previous backslashed line
            if backslashed:
                output = backslashed + output
                backslashed = ''
            
            # add to stack if backslashed or delete stack otherwise
            if output.strip().endswith("\\"):
                backslashed += output.rstrip('\\')
                continue
            else:
                backslashed = ''

            if output.startswith('!'):
                do_bash(output)
                continue

             # is this just a terrible idea?
            if output.startswith('py '):

                output = output[3:].strip().strip("'").strip('"')
            
                for k, v in objs.__dict__.items():
                    locals()[k] = v
                exec(output, globals(), locals())
                for k, v in locals().items():
                    if hasattr(objs, k):
                        setattr(objs, k, v)
                continue

            # tokenise command with quotations preserved
            tokens = shlex.split(output, comments=True)

            nested_tokens = nest_on_semicolon(tokens)

            for tokens in nested_tokens:
                if debug:
                    print('command', tokens)
                
                # give info if it is an info command
                if len(tokens) == 1 or tokens[0] == 'jupyter':
                    if tokens[0] == 'set':
                        set_something([])
                    else:
                        single_command_print(tokens)
                    continue

                # otherwise, run the command and reset the stack
                out = run_command(tokens)
                backslashed = ''

            # terminate if c mode
            if python_c_mode:
                break

        # exception handling: interrupt, exit or raise error...
        except KeyboardInterrupt:
            print('\nEnter ctrl+d, "exit" or "quit" to quit\n')
            backslashed = ''
            if python_c_mode:
                import sys
                sys.exit(0)

        except EOFError:
            import sys
            #print('\n\nBye!\n')
            sys.exit(0)
        except SystemExit:
            raise
        except Exception:
            if python_c_mode:
                import sys
                print('Error in "%s":\n' % ' '.join(tokens), file=sys.stderr)
                raise
            traceback.print_exc()

if __name__ == '__main__':
    import sys
    import pip
    import importlib
    import traceback
    import os

    def install(name, loc):
        """
        If we don't have a module, download it
        """
        try:
            importlib.import_module(name)
        except ImportError:
            pip.main(['install', loc])

    tabview = ('tabview', 'git+https://github.com/interrogator/tabview@93644dd1f410de4e47466ea8083bb628b9ccc471#egg=tabview')
    colorama = ('colorama', 'colorama')

    if not any(arg.lower() == 'noinstall' for arg in sys.argv):
        install(*tabview)
        install(*colorama)

    if len(sys.argv) > 1 and os.path.isfile(sys.argv[-1]):
        fromscript = sys.argv[-1]
    else:
        fromscript = False

    docker = next((i for i in sys.argv if i.startswith('docker=')), False)
    if docker:
        docker = docker.split('=', 1)[-1]
    print(sys.argv)

    debug = sys.argv[-1] == 'debug'
    interpreter(debug=debug, fromscript=fromscript, docker=docker)
