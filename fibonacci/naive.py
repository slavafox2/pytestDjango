def fibonacci_naive(n: int) -> int:
    if n == 0 or n == 1:
        return n

    return fibonacci_naive(n - 2) + fibonacci_naive(n - 1)


def fib_iterative(n):
    if n < 2:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
