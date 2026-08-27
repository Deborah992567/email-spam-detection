# Logs

This folder stores application log files, which are written here automatically at runtime instead of only being printed to the terminal.

> **Note:** Log files (`.log`) are git-ignored and not committed. This README and `.gitkeep` are tracked so the folder exists in the repository.

## Log files

| File          | Contents                                                              |
|---------------|-----------------------------------------------------------------------|
| `app.log`     | Backend runtime log (requests, training, DB init, errors, etc.)       |
| `error.log`   | Errors and warnings only                                              |
| `access.log`  | HTTP request access log for the FastAPI backend                       |
| `ml.log`      | Machine learning pipeline activity (training, prediction, evaluation) |

Each log file is automatically rotated at 5 MB and keeps up to 5 backups (e.g. `app.log.1`, `app.log.2`, ...).

## How it works

Logging is centralized in:

- `backend/app/core/logging_config.py` — backend + HTTP access logging
- `ml/utils/logging_setup.py` — ML pipeline logging

Both write to this same folder using `RotatingFileHandler`.
