
**User**

пересмотри файл @.github/workflows/tests.yml  и посмотри код для запуска тестов на github 
        run: |          
          pytest ./api/coronavstech/ -v -s 
          pytest fibonacci/ -s -v --durations=0 --cov=.

---

**Cursor**

В этом месте у тебя в GitHub Actions настроен запуск **двух наборов тестов подряд**.

### Что делает этот кусок

```yaml
- name: Run Tests
  env:
    DJANGO_SETTINGS_MODULE: coronavstech.settings
    PYTHONPATH: api/coronavstech
  run: |          
    pytest ./api/coronavstech/ -v -s 
    pytest fibonacci/ -s -v --durations=0 --cov=.
```

- **`env`**:
  - **`DJANGO_SETTINGS_MODULE: coronavstech.settings`** — говорит Django/pytest, какие настройки использовать (модуль `coronavstech/settings.py` из твоего проекта).
  - **`PYTHONPATH: api/coronavstech`** — добавляет эту папку в `sys.path`, чтобы импорты вида `from coronavstech...` работали.

- **Первая команда**:
  - **`pytest ./api/coronavstech/ -v -s`**
  - Запускает все тесты внутри каталога `api/coronavstech/`.
  - `-v` — подробный вывод (видно имена всех тестов).
  - `-s` — не перехватывать `print`, всё, что печатают тесты, будет видно в логах GitHub.

- **Вторая команда**:
  - **`pytest fibonacci/ -s -v --durations=0 --cov=.`**
  - Запускает все тесты в папке `fibonacci/`.
  - `-s`, `-v` — то же значение, что и выше.
  - `--durations=0` — показывает время выполнения **каждого** теста (поэтому ты и видишь строки с `runtime: 0.000698`).
  - `--cov=.` — собирает покрытие кода (code coverage) по всему текущему каталогу (`.` — корень репозитория).

Если хочешь, могу предложить вариант, как объединить эти вызовы в один `pytest`, или, например, выделить джобы: одну для Django, другую для Fibonacci.

