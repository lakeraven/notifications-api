# BDD tests (Python / pytest-bdd)

Gherkin features live under `features/`; step implementations are `step_defs/test_*.py`. The stack is **Poetry + pytest + pytest-bdd** (see `pyproject.toml`).

## Prerequisites

- **Python 3.13.x** and dependencies: `poetry install`
- **PostgreSQL** reachable from your test URI
- **Environment**: load the same variables you use for local dev (typically `SQLALCHEMY_DATABASE_URI` pointing at a **dedicated test database**, often `test_notification_api`)

```bash
set -a && source .env && set +a   # or your dotenv workflow
poetry run pytest tests/bdd/ -q --tb=short
```

The session-scoped `_notify_db` fixture in `tests/conftest.py` **creates the DB if missing**, runs **Alembic upgrade head**, and **drops the database when the pytest session ends**. You do not need to `dropdb` before every run unless you are debugging migration state.

## Fast iteration (prefer this)

| Goal | Command |
|------|---------|
| One module | `poetry run pytest tests/bdd/step_defs/test_v2_send_sms.py -x --tb=short` |
| One test | `poetry run pytest tests/bdd/step_defs/test_v2_send_sms.py::test_send_a_basic_sms_notification -v --tb=short` |
| Re-run failures only | `poetry run pytest tests/bdd/ --lf -q` |
| List tests without running | `poetry run pytest tests/bdd/ --collect-only -q` |

Use **`-x`** (stop on first failure) while fixing a file; avoid **`-v`** on the full tree unless you need node IDs.

## What makes runs slow (avoid)

1. **Running `tests/bdd/` repeatedly** in shell loops—each pass collects and sets up the whole suite.
2. **Nesting `pytest tests/bdd/` inside `for`/`while`** to count passes per file (that re-runs the full suite *per iteration*).
3. **Manual `dropdb test_notification_api` before every run**—only do that when you suspect a **bad migration state** or stale `alembic_version`.
4. **Pretty format on huge runs**—`-q` or `progress` is faster than printing every scenario verbosely.

## Parallel workers (`pytest-xdist`)

The project includes **pytest-xdist**. BDD tests share one DB and session fixtures; **`-n auto` can break tests** if workers contend on the same database. Prefer **serial** runs for `tests/bdd/` unless you invest in **isolated DBs per worker**.

## Skipped scenarios

`tests/bdd/conftest.py` registers **GOV.UK vs Notify.gov divergence** skips (v2 field names, missing routes, etc.). If a scenario is skipped, check `_SKIP_TESTS` and the comment block at the top of that file.

## Layout

```
tests/bdd/
├── conftest.py          # BDD-specific fixtures + skip map
├── features/            # *.feature files (by domain)
└── step_defs/
    ├── conftest.py
    └── test_*.py        # pytest-bdd step bindings
```

## Related docs

- Main testing pointers: [docs/all.md#testing](../../docs/all.md#testing)
- App test fixtures: `tests/conftest.py`, `tests/app/conftest.py`
