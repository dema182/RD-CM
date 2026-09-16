from __future__ import annotations

import re
from difflib import SequenceMatcher

_REGION = re.compile(
    r"\((?:usa|europe|japan|world|en|fr|de|es|it|eu|jp|us|ue|uee|rev\s*\d+)[^)]*\)",
    re.I,
)
_DUMP = re.compile(
    r"\[(?:!|b|f|h|p|t\+?|hack|fix|tr|a\d*)[^\]]*\]",
    re.I,
)
_PARENS = re.compile(r"\([^)]*\)|\[[^\]]*\]")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_THE = re.compile(r"^(the|a|an|der|die|das)\s+")


def normalize_title(name: str) -> str:
    stem = name.rsplit("/", 1)[-1]
    if "." in stem:
        stem = stem.rsplit(".", 1)[0]
    stem = _DUMP.sub(" ", stem)
    stem = _REGION.sub(" ", stem)
    stem = _PARENS.sub(" ", stem)
    stem = stem.replace("&", " and ").replace("'", "")
    stem = stem.lower()
    stem = _NON_ALNUM.sub(" ", stem)
    stem = _THE.sub("", stem)
    return " ".join(stem.split())


def similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return 0.92
    return SequenceMatcher(None, na, nb).ratio()


def best_title_match(filename: str, titles: list[str], threshold: float = 0.82) -> tuple[str, float] | None:
    best: tuple[str, float] | None = None
    for title in titles:
        score = similarity(filename, title)
        if best is None or score > best[1]:
            best = (title, score)
    if best and best[1] >= threshold:
        return best
    return None
