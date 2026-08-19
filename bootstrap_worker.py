#!/usr/bin/env python3
"""Safely unpack the versioned MEMOIR worker bundle into this checkout."""

from __future__ import annotations

import argparse
import tarfile
from pathlib import Path


BUNDLE = "worker_bundle.tar.gz"
TOP_LEVEL_DIRECTORIES = ("docs", "experiments", "reports", "scripts", "worker_tasks")


def safe_destination(root: Path, member_name: str) -> Path:
    destination = (root / member_name).resolve()
    if root != destination and root not in destination.parents:
        raise ValueError(f"Unsafe archive member: {member_name}")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Replace an earlier extracted bundle.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    bundle = root / BUNDLE
    if not bundle.is_file():
        raise SystemExit(f"Missing {BUNDLE}")

    existing = [name for name in TOP_LEVEL_DIRECTORIES if (root / name).exists()]
    if existing and not args.force:
        raise SystemExit(f"Refusing to replace existing paths: {', '.join(existing)}. Use --force only after review.")

    with tarfile.open(bundle, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            safe_destination(root, member.name)
            if member.issym() or member.islnk():
                raise ValueError(f"Links are not allowed in worker bundle: {member.name}")
        archive.extractall(root, members=members)

    print("Worker bundle extracted.")
    print("Next: read CLAUDE.md, choose machine-a or machine-b, then run the unit tests.")


if __name__ == "__main__":
    main()
