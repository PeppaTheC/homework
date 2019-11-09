def is_permutation(a: str, b: str) -> bool:
    """Функция определяет ялвяется ли строчка b,
       перестановкой строчки a"""
    if len(a) != len(b):
        return False
    char_counter = dict.fromkeys(a, 0)
    for char in a:
        char_counter[char] += 1
    for char in b:
        if char not in char_counter or char_counter[char] == 0:
            return False
        char_counter[char] -= 1
    return True


def test():
    assert is_permutation('', '')
    assert not is_permutation('', '1')
    assert not is_permutation('Abc', 'abc')
    assert not is_permutation('123', '')
    assert is_permutation('123', '321')
    assert not is_permutation('hello  EPAM', 'hello    EPAM')


if __name__ == '__main__':
    test()