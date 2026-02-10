#!/usr/bin/env python3
"""
Extract selected columns from a Rosetta scorefile (.sc) to CSV.

Outputs columns (in order):
description,
number (zero-padded digit group from description),
total_score,
dG_separated,
dSASA_int,
dG_separated/dSASAx100,
sc_value
"""

from pathlib import Path
import re
import csv

INFILE = Path("./interfaces.sc")
OUTFILE = Path("selected_rosetta_scores.csv")

WANTED = [
    "total_score",
    "dG_separated",
    "dSASA_int",
    "dG_separated/dSASAx100",
    "sc_value",
]


def extract_number(description: str) -> str:
    """
    Extract the first contiguous digit group from description
    and preserve leading zeros (e.g. '03', '10', '46').

    Returns empty string if no digits found.
    """
    match = re.search(r"(\d+)", description)
    return match.group(1) if match else ""


def parse_rosetta_scorefile(path: Path):
    header = None
    rows = []

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("SCORE:"):
                continue

            parts = line.split()
            payload = parts[1:]

            # Header line
            if header is None and "description" in payload:
                header = payload
                continue

            if header is None:
                continue

            if len(payload) != len(header):
                continue

            rows.append(dict(zip(header, payload)))

    if header is None:
        raise RuntimeError("Could not find SCORE header line.")
    if not rows:
        raise RuntimeError("No SCORE rows found.")

    return rows


def main():
    rows = parse_rosetta_scorefile(INFILE)

    out_cols = ["description", "number"] + WANTED

    with OUTFILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        writer.writeheader()

        for r in rows:
            desc = r.get("description", "")
            num = extract_number(desc)

            out = {
                "description": desc,
                "number": num,
            }
            for c in WANTED:
                out[c] = r.get(c, "")
            writer.writerow(out)

    print(f"Wrote {len(rows)} rows to {OUTFILE.resolve()}")


if __name__ == "__main__":
    main()
