import pytest

from fibonacci import naive as fib

@pytest.mark.skipif(1 < 2, reason = "Код ветвистый")
def test_naive_skip()-> None:
    res = fib.fibonacci_naive(n = 4)
    print(f"---тест проходит и выводит =  {res}")
    assert res == 3

def test_iterative() -> None:
    res = fib.fib_iterative(n = 4)
    assert res == 3


@pytest.mark.parametrize("n, expected", [(0,0), (1,1), (2,1), (20,6765)])
def test_iterative_parametrize(n: int, expected: int)->None:
    res = fib.fib_iterative(n)
    assert res == expected

