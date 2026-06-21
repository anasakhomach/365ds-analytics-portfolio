from __future__ import annotations

import os
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_DIR.parents[1]
CATALOG_PATH = APP_DIR / "catalog" / "projects.yaml"
PUBLIC_DATA_DIR = APP_DIR / "data"
DEFAULT_INDEX_DIR = Path(os.getenv("LEARNING_HUB_INDEX_DIR", APP_DIR / ".index")).resolve()
DEFAULT_CHROMA_DIR = Path(os.getenv("LEARNING_HUB_CHROMA_DIR", APP_DIR / ".chroma")).resolve()
REPOSITORY_URL = os.getenv(
    "LEARNING_HUB_REPOSITORY_URL",
    "https://github.com/anasakhomach/365ds-analytics-portfolio",
).rstrip("/")


def repo_path(relative_path: str | Path) -> Path:
    return (REPO_ROOT / relative_path).resolve()


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
