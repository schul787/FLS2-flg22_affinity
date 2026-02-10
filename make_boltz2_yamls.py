import os
import re
import csv
import yaml

# file paths
PEPTIDE_CSV = "./fls2_ligands.csv"
BASE_YAML = "./fls2.yaml"
OUTDIR = "./inputs"

os.makedirs(OUTDIR, exist_ok=True)

# ====== load base yaml ======
with open(BASE_YAML, "r") as f:
    base_yaml = yaml.safe_load(f)

if "sequences" not in base_yaml:
    raise RuntimeError("Base YAML must contain a top-level 'sequences' key")

# ====== process CSV ======
with open(PEPTIDE_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        # pull required columns
        number = int(row["Number"])
        sequence = row["Sequence"]

        # clean sequence: remove whitespace/newlines, uppercase
        sequence = re.sub(r"\s+", "", sequence).upper()

        # zero-padded index
        tag = f"{number:02d}"
        outname = f"fls2_peptide{tag}.yaml"
        outpath = os.path.join(OUTDIR, outname)

        # copy base yaml (avoid mutating original)
        doc = dict(base_yaml)
        doc["sequences"] = list(base_yaml["sequences"])

        # add ligand as chain B
        doc["sequences"].append(
            {
                "protein": {
                    "id": "B",
                    "sequence": sequence
                }
            }
        )

        # write yaml
        with open(outpath, "w") as out:
            yaml.safe_dump(doc, out, sort_keys=False, width=10**9)

        print(f"Wrote {outpath}")

print("Done.")

