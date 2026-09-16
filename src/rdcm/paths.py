from __future__ import annotations

import os
import sys
from pathlib import Path


def config_dir() -> Path:
    path = Path.home() / ".config" / "rd-cm"
    path.mkdir(parents=True, exist_ok=True)
    return path


def cache_dir() -> Path:
    path = Path.home() / ".cache" / "rd-cm"
    path.mkdir(parents=True, exist_ok=True)
    return path


def cache_version_dir(version: str = "v1") -> Path:
    path = cache_dir() / version
    path.mkdir(parents=True, exist_ok=True)
    return path


def log_dir() -> Path:
    path = Path.home() / ".local" / "state" / "rd-cm" / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def settings_path() -> Path:
    return config_dir() / "settings.json"


def bundled_dir() -> Path:
    """Directory that contains bundled binaries (RAHasher) and data files."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    vendor = repo_root / "vendor"
    if vendor.is_dir():
        return repo_root
    return here.parent


def resource_path(*parts: str) -> Path:
    base = bundled_dir()
    candidate = base.joinpath(*parts)
    if candidate.exists():
        return candidate
    pkg = Path(__file__).resolve().parent.joinpath(*parts)
    return pkg


def rahasher_binary() -> Path | None:
    env = os.environ.get("RDCM_RAHASHER")
    if env:
        p = Path(env)
        if p.is_file():
            return p
    names = ("RAHasher", "rahasher")
    search = [
        bundled_dir() / "vendor" / "RAHasher",
        bundled_dir() / "RAHasher",
        Path(__file__).resolve().parents[2] / "vendor" / "RAHasher",
        Path("/usr/bin/RAHasher"),
        Path("/usr/local/bin/RAHasher"),
    ]
    for path in search:
        if path.is_file() and os.access(path, os.X_OK):
            return path
    from shutil import which

    for name in names:
        found = which(name)
        if found:
            return Path(found)
    return None
