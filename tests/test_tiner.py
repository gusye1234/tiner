import pytest
from tiner import tiner
import threading
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
    assert (tiner.get("test:block")[0] - d) < 1e-3
    assert tiner.get("test:block")[1] == 1

    sum_d = 0.
    for _ in range(loop_times):
        with tiner("test:loop"):
            s = perf_counter()
            sleep(duration)
            d = perf_counter() - s
        sum_d += d
    assert (tiner.get("test:loop")[0] - sum_d) < 1e-3
    assert tiner.get("test:loop")[1] == loop_times
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
    tiner.enable()
    tiner.get('t1')
    with tiner("t3"):
        sleep(duration)
    with pytest.raises(KeyError):
        tiner.get("t2")
    tiner.get("t1")
    tiner.get("t3")

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

@tiner_reset
def test_table_average():
    duration = 0.001
    loop_times = 10
    for _ in range(loop_times):
        with tiner("t1"):
            sleep(duration)
        with tiner("t2"):
            sleep(duration)

        with tiner("t1"):
            sleep(duration)
    
    tiner.table()
    tiner.table(average=True)
    tiner.table(verbose=True)
    tiner.table(average=True, verbose=True)

@tiner_reset
def test_threadings():
    duration = 0.1
    test_t = 5

    def log_func():
        with tiner("test:thread"):
            sleep(duration)

    threads = []
    for _ in range(test_t):
        x = threading.Thread(target=log_func,)
        threads.append(x)
        x.start()
    for x in threads:
        x.join()
    tiner.table(verbose=True)

@tiner_reset
def test_synchronize():
    duration = 0.01
    loop_times = 5
    syn_counts = 0
    
    def syn_func():
        nonlocal syn_counts
        syn_counts += 1

    for _ in range(loop_times):
        with tiner("test:loop", synchronize=syn_func):
            sleep(duration)
    
    assert syn_counts == loop_times