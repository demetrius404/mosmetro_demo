from multiprocessing import Pool
from time import monotonic
from random import randint
import requests


def perf(n):
    d = randint(0, 10)
    endpoint = "http://127.0.0.1:8181/metro/news?days={0}".format(d)
    start_time = monotonic()
    print("starting ... {0} {1}".format(n, endpoint))
    for _ in range(n):
        requests.get(endpoint)
    exec_time = monotonic() - start_time
    rps_total = n / exec_time
    return n, d, exec_time, rps_total


if __name__ == "__main__":
    req_load = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
    # req_load = [100, 200, 300, 400]
    pool = Pool(processes=5)
    result = pool.map(perf, req_load)
    exec_total = 0
    for i in result:
        exec_total += i[2]  # exec time
        print("requests: {0}, days: {1}, exec: {2:.3f}, rps: {3:.0f}".format(*i))
    print("requests: {0}, avg rps: {1:.0f}".format(sum(req_load), sum(req_load) / exec_total))
