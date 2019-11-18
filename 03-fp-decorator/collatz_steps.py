def collatz_steps(n):
    collatz = lambda n, counter: collatz(n // 2, counter + 1) \
        if not n % 2 else collatz(3 * n + 1, counter + 1) if n > 1 else counter
    return collatz(n, 0)


def test():
    assert collatz_steps(16) == 4
    assert collatz_steps(12) == 9
    assert collatz_steps(1000000) == 152


if __name__ == '__main__':
    test()
