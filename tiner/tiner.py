import os
from collections import defaultdict
from typing import List
import inspect
import threading
from contextlib import ContextDecorator
from functools import partial
from unicodedata import name
import threading
from .utils import getline, sanity_check


class tiner(ContextDecorator):
    """
    Time context manager for code block
        with tiner():
            do something
    """
    from time import perf_counter
    from tabulate import tabulate

    get_time = perf_counter
    fmt_table = partial(tabulate, headers='firstrow', tablefmt='fancy_grid')
    __NAMED_INFO = defaultdict(dict)  # global info record
    __thread_lock = threading.Lock()
    __enable = True
    print = print

    @staticmethod
    def table(blocks: List = None, verbose=False, average=False):
        if blocks is None:
            blocks = list(tiner.__NAMED_INFO.keys())
        if not verbose:
            cols = [['Block', 'Time(s)', "Hits"]]
            for key in blocks:
                cols.append((key, *tiner.get(key)))
            if average:
                cols = [(p[0], p[1] / (p[2] + 1e-14), p[2]) for p in cols[1:]]
                cols.insert(0, ['Block', 'Aver. time(s)', "Hits"])
            tiner.print(tiner.fmt_table(cols))
            return
        for key in blocks:
            sanity_check(key, tiner.__NAMED_INFO)
            tiner.print(key)
            cols = [['File', 'Line', 'Time(s)', "Hits"]]
            for pack in sorted(tiner.__NAMED_INFO[key].keys()):
                t = tiner.__NAMED_INFO[key][pack]
                cols.append((pack[0], pack[1], *t))
            if average:
                cols = [(*p[0:2], p[2] / (p[3] + 1e-14), p[3])
                        for p in cols[1:]]
                cols.insert(0, ['Block', 'Line', 'Thread',
                            'Aver. time(s)', "Hits"])
            tiner.print(tiner.fmt_table(cols))

    @staticmethod
    def zero(blocks: List = None):
        if blocks is None:
            blocks = list(tiner.__NAMED_INFO.keys())
        for key in blocks:
            sanity_check(key, tiner.__NAMED_INFO)
            with tiner.__thread_lock:
                del tiner.__NAMED_INFO[key]

    @staticmethod
    def get(name: str):
        sanity_check(name, tiner.__NAMED_INFO)
        return sum([p[0] for p in tiner.__NAMED_INFO[name].values()]), sum([p[1] for p in tiner.__NAMED_INFO[name].values()])

    @staticmethod
    def disable():
        with tiner.__thread_lock:
            tiner.__enable = False

    @staticmethod
    def enable():
        with tiner.__thread_lock:
            tiner.__enable = True

    def __init__(self, name: str, synchronize=lambda: None):
        if not tiner.__enable:
            return
        frame = inspect.currentframe().f_back
        filename, lineno = getline(frame)
        pack = (filename, lineno)
        if pack not in tiner.__NAMED_INFO[name]:
            tiner.__NAMED_INFO[name][pack] = [0, 0]
        self.pack = pack
        self.named = name

        self.synchronize = synchronize

    def __enter__(self):
        if tiner.__enable:
            self.start = tiner.get_time()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not tiner.__enable:
            return 
        self.synchronize()
        duration = tiner.get_time() - self.start
        with tiner.__thread_lock:
            tiner.__NAMED_INFO[self.named][self.pack][0] += duration
            tiner.__NAMED_INFO[self.named][self.pack][1] += 1
