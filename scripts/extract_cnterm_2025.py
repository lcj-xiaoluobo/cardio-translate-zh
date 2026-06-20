#!/usr/bin/env python3
"""Extract the user-designated authoritative term pairs from CNTERM 2025 text.

Usage:
    python3 extract_cnterm_2025.py INPUT_PDF_OR_TEXT OUTPUT_DIR

PDF input requires pdftotext. Text input should be produced with ``pdftotext -layout``.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ENTRY_RE = re.compile(r"^\s*(\d{2}\.\d{3})\s+(.+?)\s*$")
SECTION_RE = re.compile(r"^\s*(\d{2}(?:\.\d{2}){1,2})\s+(.+?)\s*$")
HAN_RE = re.compile(r"[\u3400-\u9fff]")
HAN_SPACE_RE = re.compile(r"(?<=[\u3400-\u9fff])\s+(?=[\u3400-\u9fff])")

SLUGS = {
    "01": "01-disciplines",
    "01.01": "01-01-branches",
    "02": "02-epidemiology",
    "03.01": "03-01-histology",
    "03.02": "03-02-anatomy",
    "03.03": "03-03-physiology",
    "03.04": "03-04-pathology",
    "03.05": "03-05-symptoms-signs",
    "03.06": "03-06-tests-devices",
    "04.01": "04-01-heart-failure",
    "04.02": "04-02-arrhythmia",
    "04.03": "04-03-cardiac-arrest-scd",
    "04.04": "04-04-congenital-heart-disease",
    "04.05": "04-05-hypertension",
    "04.06": "04-06-atherosclerosis-coronary",
    "04.07": "04-07-valvular-heart-disease",
    "04.08": "04-08-infective-endocarditis",
    "04.09": "04-09-myocardial-disease",
    "04.10": "04-10-pericardial-disease",
    "04.11": "04-11-aortic-peripheral-vascular",
    "04.12": "04-12-pulmonary-vascular",
    "04.13": "04-13-cardiac-tumor",
    "05.01": "05-01-pharmacotherapy-concepts",
    "05.02": "05-02-antihypertensive-drugs",
    "05.03": "05-03-antiarrhythmic-drugs",
    "05.04": "05-04-heart-failure-drugs",
    "05.05": "05-05-antiplatelet-anticoagulation",
    "05.06": "05-06-lipid-lowering-drugs",
    "06": "06-cardiovascular-rehabilitation",
    "07": "07-cardiovascular-nursing",
}

TOP_TITLES = {
    "01": "学科及分支学科",
    "02": "流行病学",
    "06": "心血管康复",
    "07": "心血管护理",
}


def split_pair(text: str) -> tuple[str, str]:
    text = " ".join(text.split())
    candidates = []
    for match in re.finditer(r"\s+([A-Za-z0-9β])", text):
        pos = match.start()
        left, right = text[:pos].strip(), text[pos:].strip()
        if HAN_RE.search(left) and not HAN_RE.search(right):
            candidates.append((left, right))
    if candidates:
        return candidates[0]
    return text, ""


def normalize_title(text: str) -> str:
    return HAN_SPACE_RE.sub("", " ".join(text.split()))


def read_source(path: Path) -> list[str]:
    if path.suffix.lower() == ".pdf":
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.splitlines()
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract the 2025 cardiovascular terminology draft into Markdown chapter files."
    )
    parser.add_argument("input", type=Path, help="Source PDF or pdftotext -layout text file")
    parser.add_argument("output_dir", type=Path, help="Output directory")
    parser.add_argument(
        "--expected-count",
        type=int,
        default=1434,
        help="Fail unless this many numbered terms are extracted (default: 1434)",
    )
    return parser.parse_args()


def escape(value: str) -> str:
    return value.replace("|", r"\|").strip()


def main() -> None:
    args = parse_args()
    source = args.input
    out_dir = args.output_dir
    lines = read_source(source)
    second_titles = {}
    for line in lines:
        section = SECTION_RE.match(line)
        if section and section.group(1).count(".") == 1:
            second_titles[section.group(1)] = normalize_title(section.group(2))

    blocks: list[tuple[str, str, list[str]]] = []
    current_section = ""
    current_title = ""
    current_entry: tuple[str, str, list[str]] | None = None

    for line in lines:
        section = SECTION_RE.match(line)
        if section and len(section.group(1).split(".")[-1]) == 2:
            current_section, current_title = section.group(1), normalize_title(section.group(2))
            continue
        entry = ENTRY_RE.match(line)
        if entry:
            if current_entry:
                blocks.append(current_entry)
            current_entry = (entry.group(1), entry.group(2), [])
            continue
        if current_entry:
            current_entry[2].append(line)
    if current_entry:
        blocks.append(current_entry)

    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    section_titles: dict[str, str] = {}
    active_section = ""
    active_title = ""

    # Walk the source again by line so headings are assigned to entries precisely.
    block_by_id = iter(blocks)
    pending = next(block_by_id, None)
    records = []
    for line in lines:
        section = SECTION_RE.match(line)
        if section and len(section.group(1).split(".")[-1]) == 2:
            active_section, active_title = section.group(1), normalize_title(section.group(2))
            continue
        entry = ENTRY_RE.match(line)
        if not entry or pending is None:
            continue
        code, first, continuation = pending
        top = code[:2]
        group = active_section if active_section.startswith(top + ".") else top
        if group.count(".") > 1:
            group = ".".join(group.split(".")[:2])
        if group not in SLUGS:
            group = top
        section_titles[group] = second_titles.get(group, TOP_TITLES.get(group, group))

        zh, en = split_pair(first)
        if en:
            extra = []
            for more in continuation:
                clean = " ".join(more.split())
                if not clean or clean.startswith("-") or "全国科学技术名词审定委员会" in clean:
                    continue
                if HAN_RE.search(clean):
                    break
                if re.search(r"[A-Za-z]", clean):
                    extra.append(clean)
                else:
                    break
            if extra:
                en = " ".join([en, *extra])
        records.append((group, code, zh, en))
        pending = next(block_by_id, None)

    # Remove only byte-for-byte repeated entries. The draft itself reuses some
    # numeric codes for different terms; preserve and report those collisions.
    records = list(dict.fromkeys(records))
    code_counts = Counter(code for _, code, _, _ in records)
    colliding_codes = sorted(code for code, count in code_counts.items() if count > 1)
    missing_pairs = [(code, zh, en) for _, code, zh, en in records if not zh or not en]
    if missing_pairs:
        raise ValueError(f"terms missing Chinese or English: {missing_pairs[:10]}")
    if len(records) != args.expected_count:
        raise ValueError(
            f"expected {args.expected_count} terms, extracted {len(records)}; refusing partial output"
        )

    for group, code, zh, en in records:
        grouped[group].append((code, zh, en))

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        old.unlink()

    index_lines = [
        "# 《心血管病学名词（2025）》最高权限术语索引",
        "",
        "> 来源：全国科学技术名词审定委员会《心血管病学名词》2025年征求意见稿。用户指定为本项目 A0 最高术语裁决来源。",
        "",
        "如本目录与其他教材、指南或项目旧译冲突，以本目录的中文名为准；定义、缩写和英文别名仍须结合原文语境。",
        "",
        f"原稿共有 {len(records)} 条名词、{len(code_counts)} 个不同编号；其中 {len(colliding_codes)} 个编号被用于不同条目。",
        "编号冲突按原稿保留，引用时必须同时写章节、编号和规范中文名。详见 `code-collisions.md`。",
        "",
        "| 官方章节 | 文件 | 条目数 |",
        "|---|---|---:|",
    ]

    for group in sorted(grouped, key=lambda value: [int(x) for x in value.split(".")]):
        slug = SLUGS[group]
        filename = f"{slug}.md"
        title = section_titles.get(group, group)
        rows = grouped[group]
        content = [
            f"# {group} {title}",
            "",
            "> 权限：A0（最高）。来源：《心血管病学名词（2025）》征求意见稿。",
            "",
            "| 编号 | 规范中文名 | English |",
            "|---|---|---|",
        ]
        content.extend(f"| {code} | {escape(zh)} | {escape(en)} |" for code, zh, en in rows)
        (out_dir / filename).write_text("\n".join(content) + "\n", encoding="utf-8")
        index_lines.append(f"| {group} {escape(title)} | `{filename}` | {len(rows)} |")

    index_lines.extend(["", f"合计：{len(records)} 条。", ""])
    (out_dir / "README.md").write_text("\n".join(index_lines), encoding="utf-8")

    collision_lines = [
        "# 原稿编号冲突",
        "",
        "> 下列编号在《心血管病学名词（2025）》征求意见稿中对应不同条目。按原稿保留，不擅自重编号。",
        "",
        "引用格式：`章节 + 编号 + 规范中文名`。",
        "",
        "| 编号 | 章节 | 规范中文名 | English |",
        "|---|---|---|---|",
    ]
    for group, code, zh, en in records:
        if code in colliding_codes:
            collision_lines.append(
                f"| {code} | {group} | {escape(zh)} | {escape(en)} |"
            )
    (out_dir / "code-collisions.md").write_text(
        "\n".join(collision_lines) + "\n", encoding="utf-8"
    )
    print(
        f"validated {len(records)} bilingual terms; "
        f"preserved {len(colliding_codes)} colliding draft codes; "
        f"generated {len(grouped)} chapter files plus two indexes"
    )


if __name__ == "__main__":
    main()
