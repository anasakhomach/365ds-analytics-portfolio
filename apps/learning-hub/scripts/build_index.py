from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.indexing import build_index, check_index_inputs
from learning_hub.settings import load_ai_settings


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the 365DS Learning Hub search index.")
    parser.add_argument("--check", action="store_true", help="Validate and summarize index inputs without writing files.")
    parser.add_argument("--index-dir", default=None, help="Optional index output directory.")
    parser.add_argument("--backend", choices=["local_tfidf", "chroma_openai_compatible"], default=None)
    parser.add_argument("--embedding-model", default=None)
    args = parser.parse_args()

    index_dir = Path(args.index_dir) if args.index_dir else None
    env_overrides = {}
    if args.backend:
        env_overrides["LEARNING_HUB_EMBEDDING_BACKEND"] = args.backend
    if args.embedding_model:
        env_overrides["LEARNING_HUB_EMBEDDING_MODEL"] = args.embedding_model
    settings = load_ai_settings({**dict(os.environ), **env_overrides})

    if args.check:
        manifest = check_index_inputs()
    elif index_dir:
        manifest = build_index(index_dir=index_dir, settings=settings)
    else:
        manifest = build_index(settings=settings)
    print(json.dumps(asdict(manifest), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
