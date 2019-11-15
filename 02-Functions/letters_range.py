def letters_range(start: str, stop: str = None, step: int = 1, **transliterations) -> list:
    """Function returns a list of letters from the letter start to the letter stop"""
    if start and not stop:
        stop = start
        start = 'a'
    start, stop = ord(start), ord(stop)
    letters_list = []
    while start < stop if step > 0 else start > stop:
        char = chr(start)
        if char not in transliterations:
            letters_list.append(char)
        else:
            letters_list.append(str(transliterations[char]))
        start += step
    return letters_list


def test():
    assert letters_range('b', 'w', 2) == ['b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', 'r', 't', 'v']
    assert letters_range('g') == ['a', 'b', 'c', 'd', 'e', 'f']
    assert letters_range('g', 'p') == ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
    assert letters_range('g', 'p', **{'l': 7, 'o': 0}) == ['g', 'h', 'i', 'j', 'k', '7', 'm', 'n', '0']
    assert letters_range('p', 'g', -2) == ['p', 'n', 'l', 'j', 'h']
    assert letters_range('a') == []


if __name__ == '__main__':
    test()
