import pytest
from fibonacci.decorator.my_decorator import (
    get_list_of_kwargs_for_function,
    my_parametrized,
)


def test_get_list_of_kwargs_for_function_simple():
    identifiers = "a,b"
    values = [(1, 2), (3, 4)]
    result = get_list_of_kwargs_for_function(identifiers, values)
    assert result == [{"a": 1, "b": 2}, {"a": 3, "b": 4}]


def test_get_list_of_kwargs_for_function_three_args():
    identifiers = "x,y,z"
    values = [(1, 2, 3), (4, 5, 6)]
    result = get_list_of_kwargs_for_function(identifiers, values)
    assert result == [
        {"x": 1, "y": 2, "z": 3},
        {"x": 4, "y": 5, "z": 6},
    ]


def test_my_parametrized_calls_function_with_all_values():
    calls = []

    @my_parametrized("a,b", [(1, 2), (10, 20)])
    def func(a: int, b: int) -> None:
        calls.append((a, b))

    # декоратор возвращает обёртку без аргументов
    func()

    assert calls == [(1, 2), (10, 20)]


def test_my_parametrized_works_with_single_argument():
    calls = []

    @my_parametrized("x", [(5,), (42,)])
    def func(x: int) -> None:
        calls.append(x)

    func()

    assert calls == [5, 42]