#!/usr/bin/env python3
"""
Convert Boltz2 output CIFs to PDBs.

Expected layout (default):
  SRC_BASE/fls2_peptide01/fls2_peptide01_model_0.cif
  ...
  SRC_BASE/fls2_peptide50/fls2_peptide50_model_0.cif

Outputs:
  DEST_DIR/fls2_peptide01_model_0.pdb
  ...
"""

from pathlib import Path
import sys
from Bio.PDB import MMCIFParser, PDBIO

# =========================
# DEFINE DIRECTORY PATHS
# =========================

# Base directory containing fls2_peptide## folders
SRC_BASE = Path("/mnt/home/schul787/CHE882/affinity/boltz_results_inputs/predictions")

# Output directory for all converted PDBs
DEST_DIR = Path("/mnt/home/schul787/CHE882/affinity/all_pdbs")

# Range of peptide indices
START_INDEX = 1
END_INDEX = 50

# =========================
# CONVERT CIFS TO PDBS AND SAVE TO DEST_DIR
# =========================

def cif_to_pdb(cif_path: Path, pdb_path: Path) -> None:
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure(cif_path.stem, str(cif_path))

    io = PDBIO()
    io.set_structure(structure)
    io.save(str(pdb_path))


def main() -> int:
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    n_ok = 0
    n_missing = 0
    n_failed = 0

    for i in range(START_INDEX, END_INDEX + 1):
        tag = f"{i:02d}"
        run_dir = SRC_BASE / f"fls2_peptide{tag}"
        cif_file = run_dir / f"fls2_peptide{tag}_model_0.cif"

        if not cif_file.exists():
            print(f"[MISSING] {cif_file}")
            n_missing += 1
            continue

        pdb_file = DEST_DIR / f"{cif_file.stem}.pdb"

        try:
            cif_to_pdb(cif_file, pdb_file)
            print(f"[OK] {cif_file} -> {pdb_file}")
            n_ok += 1
        except Exception as e:
            print(f"[FAILED] {cif_file}: {e}", file=sys.stderr)
            n_failed += 1

    print(f"\nDone. OK={n_ok}, MISSING={n_missing}, FAILED={n_failed}")
    return 0 if n_failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
