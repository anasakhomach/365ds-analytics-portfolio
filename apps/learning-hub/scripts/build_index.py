from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.indexing import build_local_index, check_index_inputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the 365DS Learning Hub search index.")
    parser.add_argument("--check", action="store_true", help="Validate and summarize index inputs without writing files.")
    parser.add_argument("--index-dir", default=None, help="Optional index output directory.")
    args = parser.parse_args()

    index_dir = Path(args.index_dir) if args.index_dir else None
    manifest = check_index_inputs() if args.check else build_local_index(index_dir=index_dir) if index_dir else build_local_index()
    print(json.dumps(asdict(manifest), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
