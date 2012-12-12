# -*- coding: utf-8 -*-

import time
from   functools import wraps

ELAPSED_DATA = {}

"""
Para usar:
    @elapsed
    def your_function(...):
        ...
Para imprimir os tempos:
    print_elapsed_data()
Para limpar os tempos:
    clear_elapsed_data()
"""
def elapsed(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        if fn.__name__ not in ELAPSED_DATA:
            ELAPSED_DATA[fn.__name__] = [0, []]
        ELAPSED_DATA[fn.__name__][0] += 1
        ELAPSED_DATA[fn.__name__][1].append(elapsed_time)
        return ret
    return with_profiling

def get_elapsed_data():
    ret = ''
    for fname, data in ELAPSED_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        ret += (('\n' if ret else '') + "    %d %s. " % (data[0], 'execucao'
                                              if data[0] < 2 else 'execucoes'))
        ret += (('\n' if ret else '') + 'Tempo: %.3f (Max), %.3f (Media)' %
                                                    (avg_time/60, max_time/60))
    return ret

def print_elapsed_data():
    for fname, data in ELAPSED_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        print "    %d %s. " % (data[0], 'execucao'
                                              if data[0] < 2 else 'execucoes'),
        print 'Tempo: %.3f (Max), %.3f (Media)' % (avg_time/60, max_time/60)

def clear_elapsed_data():
    global ELAPSED_DATA
    ELAPSED_DATA = {}