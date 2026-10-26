# Agent CI Fixture

Небольшой тестовый репозиторий для проверки Directum Log Analyzer и его CI watcher.

## Намеренная ошибка

В `calculator.py` функция `subtract()` складывает числа вместо вычитания. Поэтому CI должен завершиться с ошибкой.

## Локальная проверка

```bash
cd /Users/dima/Documents/programming/agent-ci-fixture
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -q
```

Ожидаемый результат до исправления: 2 failed.

## Публикация на GitHub

Создайте пустой репозиторий на GitHub, затем выполните:

```bash
cd /Users/dima/Documents/programming/agent-ci-fixture
git init -b main
git add .
git commit -m "test: add failing CI fixture"
git remote add origin https://github.com/<USERNAME>/<REPOSITORY>.git
git push -u origin main
```

После push вкладка Actions должна показать красный workflow `CI`.

## Подключение watcher

В `/Users/dima/Documents/programming/PP/.env` укажите:

```env
GITHUB_TOKEN=ваш_токен_с_правом_чтения_actions
GITHUB_REPOSITORY=<USERNAME>/<REPOSITORY>
GITHUB_DEFAULT_BRANCH=main
CI_POLL_INTERVAL_SECONDS=30
```

Затем в отдельном терминале из проекта агента:

```bash
cd /Users/dima/Documents/programming/PP
source .venv/bin/activate
python -m tools.watch_ci --repo /Users/dima/Documents/programming/agent-ci-fixture --once
```

Watcher найдёт failed run, скачает логи GitHub Actions и передаст их GigaChat вместе с исходниками fixture. Он только напечатает анализ и не изменит Git.

## Применение исправления

После анализа запустите сервер агента:

```bash
cd /Users/dima/Documents/programming/PP
source .venv/bin/activate
uvicorn app.api:app --reload
```

Откройте `http://127.0.0.1:8000/`, загрузите файл с ошибкой или используйте лог из Actions, укажите корень:

```text
/Users/dima/Documents/programming/agent-ci-fixture
```

Нажмите «Предложить исправление», проверьте diff и только после этого нажмите «Применить изменение». Должно быть предложено заменить:

```python
return left + right
```

на:

```python
return left - right
```

После применения проверьте локально:

```bash
cd /Users/dima/Documents/programming/agent-ci-fixture
.venv/bin/pytest -q
```

Затем проверьте изменения и отправьте их сами:

```bash
git diff
git status
git add calculator.py
git commit -m "fix: correct subtraction in calculator"
git push
```

После push GitHub Actions должен стать зелёным. Для первого эксперимента не давайте агенту token с правом записи: watcher и локальный режим требуют только чтение.
