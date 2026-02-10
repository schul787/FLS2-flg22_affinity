"""
Create a sorted Rosetta input list from a directory of PDB files.
"""

from pathlib import Path

# Directory containing PDBs (relative to where you run the script)
PDB_DIR = Path("../all_pdbs")
OUTFILE = Path("in_pdbs.txt")

if not PDB_DIR.is_dir():
    raise FileNotFoundError(f"Directory not found: {PDB_DIR}")

pdbs = sorted(p for p in PDB_DIR.iterdir() if p.suffix.lower() == ".pdb")

if not pdbs:
    raise RuntimeError(f"No .pdb files found in {PDB_DIR}")

with OUTFILE.open("w") as f:
    for pdb in pdbs:
        f.write(str(pdb.resolve()) + "\n")

print(f"Wrote {len(pdbs)} PDB paths to {OUTFILE}")