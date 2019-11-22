from functools import wraps, lru_cache
from time import monotonic
from dataclasses import dataclass
import math
import sys

sys.setrecursionlimit(10 ** 6)


@dataclass
class Results:
    __slots__ = {'count', 'time', 'name'}
    count: int
    time: float

    def __repr__(self):
        return f'{self.name}\nNumber of calls: {self.count}\ntime: {self.time} '

    def __gt__(self, other):
        return self.time > other

    def __lt__(self, other):
        return self.time < other

    def __ge__(self, other):
        return self.time >= other

    def __le__(self, other):
        return self.time <= other


results_recursion = Results(0, 0)
results_recursion_with_cache = Results(0, 0)
results_ugly = Results(0, 0)
results_dynamic = Results(0, 0)
results_local_cache = Results(0, 0)


def count_and_time(results: Results):
    def my_decorator(func):
        start = None
        results.count = 0
        results.name = func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal start
            if start is None:
                start = monotonic()
            results.count += 1
            result = func(*args, **kwargs)
            end = monotonic()
            results.time = end - start
            return result

        return wrapper

    return my_decorator


@count_and_time(results_recursion)
def recursion_fibonacci(n):
    return recursion_fibonacci(n - 1) + recursion_fibonacci(n - 2) if n > 2 else 1


@count_and_time(results_recursion_with_cache)
@lru_cache(maxsize=5)
def recursion_fibonacci_with_cache(n):
    return recursion_fibonacci_with_cache(n - 1) + recursion_fibonacci_with_cache(n - 2) if n > 2 else 1


@count_and_time(results_ugly)
def ugly_fib(n):
    SQRT5 = math.sqrt(5)
    PHI = (SQRT5 + 1) / 2
    return int(PHI ** n / SQRT5 + 0.5)


@count_and_time(results_dynamic)
def dynamic_fib(n):
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
    return a


N = {0: 0, 1: 1}


@count_and_time(results_local_cache)
def local_cache_fib(n):
    if n in N:
        return N[n]
    N[n] = local_cache_fib(n - 1) + local_cache_fib(n - 2)
    return N[n]


def find_best():
    global N
    # print(recursion_fibonacci(10 ** 3)) # too slow
    # print(results_recursion)
    print(recursion_fibonacci(30))  # too slow
    print(results_recursion)  # took the 5th place

    # round one
    print("ROUND ONE")
    recursion_fibonacci_with_cache(10 ** 3)  # took the 4th place
    print(results_recursion_with_cache)
    ugly_fib(10 ** 3)
    print(results_ugly)
    dynamic_fib(10 ** 3)
    print(results_dynamic)
    local_cache_fib(10 ** 3)
    print(results_local_cache)
    print('Slowest:', max(results_recursion_with_cache, results_ugly, results_dynamic, results_local_cache))

    # round two
    print('ROUND TWO')
    N = {0: 0, 1: 1}
    # ugly_fib(10 ** 4) # count work with big numbers, took the 3rd place
    # print(results_ugly)
    dynamic_fib(10 ** 4)
    print(results_dynamic)
    # local_cache_fib(10 ** 4) # doesn't either work, 2nd place

    print(f'The best: {results_dynamic}')


if __name__ == '__main__':
    find_best()
