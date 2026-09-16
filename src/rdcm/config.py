from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

from .paths import settings_path

PLACEHOLDER_KEYS = {"", "YOUR_API_KEY", "changeme", "placeholder"}


class Settings:
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        data = data or {}
        self.ra_api_key: str = str(data.get("ra_api_key") or "")
        self.ra_username: str = str(data.get("ra_username") or "")
        self.retrodeck_path: str = str(data.get("retrodeck_path") or "")
        self.cache_days: int = int(data.get("cache_days") or 7)
        self.language: str = str(data.get("language") or "de")

    def to_dict(self) -> dict[str, Any]:
        return {
            "ra_api_key": self.ra_api_key,
            "ra_username": self.ra_username,
            "retrodeck_path": self.retrodeck_path,
            "cache_days": self.cache_days,
            "language": self.language,
        }

    @property
    def has_api_key(self) -> bool:
        key = self.ra_api_key.strip()
        return bool(key) and key not in PLACEHOLDER_KEYS


def load_settings() -> Settings:
    path = settings_path()
    if not path.is_file():
        return Settings()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return Settings()
        return Settings(data)
    except (OSError, json.JSONDecodeError):
        return Settings()


def save_settings(settings: Settings) -> Path:
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(settings.to_dict(), indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    return path


def redact(text: str, secret: str) -> str:
    if not secret or len(secret) < 4:
        return text
    return text.replace(secret, "***")
