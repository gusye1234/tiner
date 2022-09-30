from tiner import tiner
from time import sleep, perf_counter


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
