#!/usr/bin/env python3
"""Validate the generated A0 corpus and the hand-maintained extension libraries."""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
TERMINOLOGY = REFERENCES / "terminology"
A0_DIR = TERMINOLOGY / "cnterm-2025"
TERM_ROW = re.compile(r"^\| (\d{2}\.\d{3}) \| (.*?) \| (.*?) \|$")


def normalize_english(value: str) -> str:
    value = value.split(",", 1)[0].lower().strip()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalize_chinese(value: str) -> str:
    return re.sub(r"[\s-]+", "", value)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    official: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    codes: list[str] = []
    rows = 0

    chapter_files = sorted(
        path for path in A0_DIR.glob("*.md")
        if path.name not in {"README.md", "code-collisions.md"}
    )
    if len(chapter_files) != 30:
        fail(errors, f"expected 30 A0 chapter files, found {len(chapter_files)}")

    for path in chapter_files:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = TERM_ROW.match(line)
            if not match:
                continue
            code, chinese, english = (part.strip() for part in match.groups())
            rows += 1
            codes.append(code)
            if not chinese or not english:
                fail(errors, f"{path}:{line_number}: empty bilingual field")
            official[normalize_english(english)].append((chinese, code, path.name))

    if rows != 1434:
        fail(errors, f"expected 1434 A0 terms, found {rows}")
    counts = Counter(codes)
    if len(counts) != 1374:
        fail(errors, f"expected 1374 distinct draft codes, found {len(counts)}")
    collisions = {code for code, count in counts.items() if count > 1}
    if len(collisions) != 59:
        fail(errors, f"expected 59 reused draft codes, found {len(collisions)}")

    index = (REFERENCES / "cardiovascular-terminology.md").read_text(encoding="utf-8")
    for relative in re.findall(r"`(terminology/[^`]+(?:\.md|/))`", index):
        target = REFERENCES / relative
        if relative.endswith("/"):
            if not target.is_dir():
                fail(errors, f"missing routed directory: references/{relative}")
        elif not target.is_file():
            fail(errors, f"missing routed file: references/{relative}")

    extension_files = [
        path for path in TERMINOLOGY.rglob("*.md")
        if A0_DIR not in path.parents and path.name != "electrophysiology-arrhythmia.md"
    ]
    for path in extension_files:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "| A |" in line:
                fail(errors, f"{path}:{line_number}: obsolete authority marker A; use A0")
            if not line.startswith("| ") or line.startswith(("| English", "|---")):
                continue
            columns = [part.strip() for part in line.strip("|").split("|")]
            if len(columns) < 3:
                continue
            english, chinese, marker = columns[:3]
            key = normalize_english(english)
            if marker == "A0" and key not in official:
                fail(errors, f"{path}:{line_number}: A0 term has no exact official English match: {english}")
            if key in official and all(
                normalize_chinese(chinese) != normalize_chinese(item[0])
                for item in official[key]
            ):
                expected = " / ".join(item[0] for item in official[key])
                fail(errors, f"{path}:{line_number}: conflicts with A0: {english} -> {chinese}; expected {expected}")

    if errors:
        print("Terminology validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Terminology validation passed: "
        f"{rows} A0 terms, {len(counts)} distinct codes, "
        f"{len(collisions)} reused codes, {len(extension_files)} extension files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
