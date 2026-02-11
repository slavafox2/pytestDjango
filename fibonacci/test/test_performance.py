import pytest

from fibonacci.dynamic import fibonacci_dynamic_v2
from fibonacci.conftest import track_performance


# Как запускать только performance тесты:
# 1. pytest -m performance
# Запустить всё, кроме performance:
# 2. pytest -m "not performance"
# Только этот файл:
# 3. pytest fibonacci/test/test_performance.py -v -s

@pytest.mark.performance
@track_performance
def test_performance():
    fibonacci_dynamic_v2(1000)
