from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable

from .config import redact
from .paths import log_dir


class RedactingFilter(logging.Filter):
    def __init__(self, secrets: Callable[[], list[str]]) -> None:
        super().__init__()
        self._secrets = secrets

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for secret in self._secrets():
            if secret:
                msg = redact(msg, secret)
        record.msg = msg
        record.args = ()
        return True


def setup_logging(secret_provider: Callable[[], list[str]] | None = None) -> Path:
    log_path = log_dir() / f"rd-cm-{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("rdcm")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    secrets = secret_provider or (lambda: [])
    filt = RedactingFilter(secrets)
    fh.addFilter(filt)
    sh.addFilter(filt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return log_path


def get_logger() -> logging.Logger:
    return logging.getLogger("rdcm")
