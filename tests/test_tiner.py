import pytest
from tiner import tiner
from functools import wraps
from time import sleep, perf_counter


def tiner_reset(func):
    @wraps(func)
    def inner(*args, **kwargs):
        tiner.zero()
        tiner.enable()
        func(*args, **kwargs)
    return inner


@tiner_reset
def test_time_mining():
    duration = 0.1
    loop_times = 5

    with tiner("test:block"):
        s = perf_counter()
        sleep(duration)
        d = perf_counter() - s
    assert (tiner.get("test:block") - d) < 1e-3

    sum_d = 0.
    for _ in range(loop_times):
        with tiner("test:loop"):
            s = perf_counter()
            sleep(duration)
            d = perf_counter() - s
        sum_d += d
    assert (tiner.get("test:loop") - sum_d) < 1e-3
    tiner.table(verbose=True)


@tiner_reset
def test_decorator():
    duration = 0.1

    @tiner("func time")
    def f():
        sleep(duration)
    f()
    tiner.table(blocks=['func time'], verbose=True)


@tiner_reset
def test_zero():
    duration = 0.1

    with tiner("t1"):
        sleep(duration)
    with tiner("t2"):
        sleep(duration)

    tiner.zero(blocks=['t1'])
    with pytest.raises(KeyError):
        tiner.get("t1")
    tiner.get("t2")
    tiner.zero()
    with pytest.raises(KeyError):
        tiner.get("t2")


@tiner_reset
def test_disable():
    duration = 0.1

    with tiner("t1"):
        sleep(duration)
    tiner.disable()
    with tiner("t2"):
        sleep(duration)

    tiner.get('t1')
    with pytest.raises(KeyError):
        tiner.get("t2")


@tiner_reset
def test_table():
    duration = 0.1
    with tiner("t1"):
        sleep(duration)
    with tiner("t2"):
        sleep(duration)

    with tiner("t1"):
        sleep(duration)

    tiner.table()
    tiner.table(verbose=True)
