from collections import defaultdict
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
    __NAMED_TAPE = defaultdict(float)  # global time record

    @staticmethod
    def table(select_keys=None):
        data = [['Tape', 'Time(s)']]
        if select_keys is None:
            for key, value in tiner.__NAMED_TAPE.items():
                hint = hint + f"{key}:{value:.2f}|"
                data.append((key, value))
        else:
            for key in select_keys:
                value = tiner.__NAMED_TAPE[key]
                data.append((key, value))
        print(tiner.fmt_table(data))

    @staticmethod
    def zero(select_keys=None):
        if select_keys is None:
            for key in tiner.__NAMED_TAPE.keys():
                tiner.__NAMED_TAPE[key] = 0
        else:
            for key in select_keys:
                tiner.__NAMED_TAPE[key] = 0

    @staticmethod
    def get(name):
        return tiner.__NAMED_TAPE[name]

    def __init__(self, name, **kwargs):
        self.named = name

    def __enter__(self):
        self.start = tiner.get_time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = tiner.get_time() - self.start
        tiner.__NAMED_TAPE[self.named] += duration
