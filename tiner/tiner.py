from collections import defaultdict
from stat import filemode
from typing import List
import inspect
from contextlib import ContextDecorator
from functools import partial
from unicodedata import name
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
    __enable = True

    @staticmethod
    def table(blocks: List = None, verbose=False):
        if blocks is None:
            blocks = list(tiner.__NAMED_INFO.keys())
        if not verbose:
            data = [['Block', 'Time(s)']]
            for key in blocks:
                data.append((key, tiner.get(key)))
            print(tiner.fmt_table(data))
        else:
            for key in blocks:
                sanity_check(key, tiner.__NAMED_INFO)
                print(key)
                cols = [['File', 'Line', 'Time(s)']]
                for pack, t in tiner.__NAMED_INFO[key].items():
                    cols.append((pack[0], pack[1], t))
                print(tiner.fmt_table(cols))

    @staticmethod
    def zero(blocks: List = None):
        if blocks is None:
            blocks = list(tiner.__NAMED_INFO.keys())
        for key in blocks:
            sanity_check(key, tiner.__NAMED_INFO)
            del tiner.__NAMED_INFO[key]

    @staticmethod
    def get(name: str):
        sanity_check(name, tiner.__NAMED_INFO)
        return sum(tiner.__NAMED_INFO[name].values())

    @staticmethod
    def disable():
        tiner.__enable = False

    @staticmethod
    def enable():
        tiner.__enable = True

    def __init__(self, name: str, **kwargs):
        if tiner.__enable:
            frame = inspect.currentframe().f_back
            filename, lineno = getline(frame)
            if (filename, lineno) not in tiner.__NAMED_INFO[name]:
                tiner.__NAMED_INFO[name][(filename, lineno)] = 0
            self.pack = (filename, lineno)
            self.named = name

    def __enter__(self):
        if tiner.__enable:
            self.start = tiner.get_time()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if tiner.__enable:
            duration = tiner.get_time() - self.start
            tiner.__NAMED_INFO[self.named][self.pack] += duration
