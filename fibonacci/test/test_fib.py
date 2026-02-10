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



from typing import Callable
import pytest
# from fibonacci.dynamic import fibonacci_dynamic, fibonacci_dynamic_v2
from fibonacci.cached import fibonacci_cached, fibonacci_lru_cached
from fibonacci.naive import fibonacci_naive


@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
@pytest.mark.parametrize(
    "fib_func",
    [
        fibonacci_naive,
        fibonacci_cached,
        fibonacci_lru_cached,
        # fibonacci_dynamic,
        # fibonacci_dynamic_v2,
    ],
)

# fib_func: Callable[[int], int]
##
# Это аннотация типа (Type Hinting). Она не меняет логику работы кода, но служит подсказкой для программиста и инструментов (например, PyCharm или MyPy).
# Вот как она расшифровывается:
# 1. fib_func
# Это имя переменной, в которую передается сама функция (как объект). В Python функции можно передавать в качестве аргументов другим функциям.
# 2. Callable
# Это тип из модуля typing. Он указывает на то, что объект можно «вызвать» (то есть поставить после него скобки () и выполнить код). Проще говоря — это функция.
# 3. [[int], int] (Внутри скобок)
# Это уточнение того, какой именно должна быть эта функция:
# [int] — список типов входящих аргументов. В данном случае мы ожидаем, что функция принимает ровно один аргумент типа int (целое число).
# , int — тип возвращаемого значения. Функция должна возвращать int.
# Простыми словами
# Запись fib_func: Callable[[int], int] говорит:
# "Переменная fib_func — это функция, которая берет на вход одно целое число и возвращает в ответ тоже целое число".
def test_fibonacci(
    time_tracker, fib_func: Callable[[int], int], n: int, expected: int
) -> None:
    res = fib_func(n)
    assert res == expected

    # Сообщение:
    # test_fibonacci[fibonacci_naive - 0 - 0]:    test_fibonacci — имя тестовой функции. fibonacci_naive — это параметра
    # fib_func(конкретная функция, которую тестируем). Первый 0 — значение параметра n. Второй 0 — значение параметра expected. То есть
    # эта строка означает: "запуск теста test_fibonacci с функцией fibonacci_naive, при n = 0 и expected = 0". А [fibonacci_naive - 1 - 1] — это тот же тест,
    # но с параметрами fib_func = fibonacci_naive, n = 1, expected = 1.