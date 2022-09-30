from collections import defaultdict
from typing import List
from functools import partial


class tiner:
    """
    Time context manager for code block
        with tiner():
            do something
    """
    from time import perf_counter
    from tabulate import tabulate

    get_time = perf_counter
    fmt_table = partial(tabulate, headers='firstrow', tablefmt='fancy_grid')
    __NAMED_BLOCK = defaultdict(float)  # global time record
    __enable = True

    @staticmethod
    def table(blocks: List = None):
        data = [['Block', 'Time(s)']]
        if blocks is None:
            for key, value in tiner.__NAMED_BLOCK.items():
                data.append((key, value))
        else:
            for key in blocks:
                value = tiner.__NAMED_BLOCK[key]
                data.append((key, value))
        print(tiner.fmt_table(data))

    @staticmethod
    def zero(blocks: List = None):
        if blocks is None:
            for key in tiner.__NAMED_BLOCK.keys():
                tiner.__NAMED_BLOCK[key] = 0
        else:
            for key in blocks:
                tiner.__NAMED_BLOCK[key] = 0

    @staticmethod
    def get(name: str):
        return tiner.__NAMED_BLOCK[name]

    @staticmethod
    def disable(name: str):
        tiner.__enable = False

    def __init__(self, name: str, **kwargs):
        if tiner.__enable:
            self.named = name

    def __enter__(self):
        if tiner.__enable:
            self.start = tiner.get_time()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if tiner.__enable:
            duration = tiner.get_time() - self.start
            tiner.__NAMED_BLOCK[self.named] += duration
