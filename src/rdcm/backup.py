from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def backup_root(retrodeck: Path) -> Path:
    return retrodeck / "backup"


def create_backup(retrodeck: Path, sources: list[Path]) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dest = backup_root(retrodeck) / stamp
    dest.mkdir(parents=True, exist_ok=True)
    for src in sources:
        if not src.exists():
            continue
        rel = _safe_rel(src, retrodeck)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, target, dirs_exist_ok=True)
        else:
            shutil.copy2(src, target)
    (dest / "MANIFEST.txt").write_text(
        "RD-CM backup\n" + "\n".join(str(s) for s in sources) + "\n",
        encoding="utf-8",
    )
    return dest


def _safe_rel(path: Path, root: Path) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return Path(path.name)
