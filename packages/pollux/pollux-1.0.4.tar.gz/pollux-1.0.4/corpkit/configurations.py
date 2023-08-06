def configurations(corpus, search, **kwargs):
    """
    Get summary of behaviour of a word

    see corpkit.corpus.Corpus.configurations() for docs
    """

    from corpkit.dictionaries.wordlists import wordlists
    from corpkit.dictionaries.roles import roles
    from corpkit.interrogator import interrogator
    from collections import OrderedDict

    if search.get('l') and search.get('w'):
        raise ValueError('Search only for a word or a lemma, not both.')

    # are we searching words or lemmata?
    if search.get('l'):
        dep_word_or_lemma = 'dl'
        gov_word_or_lemma = 'gl'
        word_or_token = search.get('l')
    else:
        if search.get('w'):
            dep_word_or_lemma = 'd'
            gov_word_or_lemma = 'g'
            word_or_token = search.get('w')

    # make nested query dicts for each semantic role
    queries = {'participant': 

                {'left_participant_in':             
                  {dep_word_or_lemma: word_or_token,
                   'df': roles.participant1,
                   'f': roles.event},

                'right_participant_in':
                  {dep_word_or_lemma: word_or_token,
                   'df': roles.participant2,
                   'f': roles.event},

                'premodified':
                  {'f': roles.premodifier, 
                   gov_word_or_lemma: word_or_token},

                'postmodified':
                  {'f': roles.postmodifier, 
                   gov_word_or_lemma: word_or_token},

                 'and_or':
                  {'f': 'conj:(?:and|or)',
                   'gf': roles.participant,
                   gov_word_or_lemma: word_or_token},
                },

               'process':

                {'has_subject':
                  {'f': roles.participant1,
                   gov_word_or_lemma: word_or_token},

                 'has_object':
                  {'f': roles.participant2,
                   gov_word_or_lemma: word_or_token},

                 'modalised_by':
                  {'f': r'aux',
                   'w': wordlists.modals,
                   gov_word_or_lemma: word_or_token},

                 'modulated_by':
                  {'f': 'advmod',
                   'gf': roles.event,
                   gov_word_or_lemma: word_or_token},

                 'and_or':
                  {'f': 'conj:(?:and|or)',
                   'gf': roles.event,                 
                   gov_word_or_lemma: word_or_token},
              
                },

               'modifier':

                {'modifies':
                  {'df': roles.modifier,
                   dep_word_or_lemma: word_or_token},

                 'modulated_by':
                  {'f': 'advmod',
                   'gf': roles.modifier,
                   gov_word_or_lemma: word_or_token},

                 'and_or':
                  {'f': 'conj:(?:and|or)',
                   'gf': roles.modifier,
                   gov_word_or_lemma: word_or_token},

                }
              }

    # allow passing in of single function
    if search.get('f'):
        if search.get('f').lower().startswith('part'):
            queries = queries['participant']
        elif search.get('f').lower().startswith('proc'):
            queries = queries['process']
        elif search.get('f').lower().startswith('mod'):
            queries = queries['modifier']
    else:
        newqueries = {}
        for k, v in queries.items():
            for name, pattern in v.items():
                newqueries[name] = pattern
        queries = newqueries
        queries['and_or'] = {'f': 'conj:(?:and|or)', gov_word_or_lemma: word_or_token}
    
    kwargs['search'] = queries
    
    # do interrogation
    data = corpus.interrogate(**kwargs)
    
    # remove result itself
    # not ideal, but it's much more impressive this way.
    return data

