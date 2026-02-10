# Predicting FLS2–Flagellin Peptide Binding Affinity

This repository contains scripts and workflows used to predict binding affinities between 50 flagellin peptides and the plant immune receptor FLS2, using a combination of Boltz2 structure prediction, PPI-Graphomer, and Rosetta InterfaceAnalyzer.  
This work was completed as part of a course project and is focused on tool setup and data preparation.

---

## Overview of the Workflow

The overall pipeline consists of the following steps:

1. Peptide set construction  
2. Boltz2 structure prediction  
3. Structure post-processing  
4. Batch affinity prediction with PPI-Graphomer  
5. Interface scoring with Rosetta InterfaceAnalyzer  
6. Score comparison and consolidation  

Each step is described below.

---

## 1. Peptide Set Construction

- A CSV file (fls2_ligands.csv) was created containing 50 flagellin peptides.
- The peptide set includes:
  - Peptides reported in the literature with known or inferred FLS2 interactions
  - Additional peptides identified via BLAST searches
  - Made-up peptide variants

---

## 2. Boltz2 Input Generation

- A Python script (make_boltz2_yamls.py) was written to:
  - Read peptide sequences from the CSV
  - Combine each peptide sequence with the FLS2 receptor sequence
  - Automatically generate a Boltz2-compatible `.yaml` input file for each peptide–FLS2 pair
- This allows Boltz2 to be run in batch mode with consistent formatting and minimal manual intervention.

---

## 3. Boltz2 Structure Prediction

- Boltz2 was run on the generated YAML inputs to predict structures of each flagellin peptide bound to FLS2.
- Each prediction produces a `.cif` structure file per peptide–receptor complex.

---

## 4. Structure Post-Processing

- A Biopython-based script (get_cif2pdb.py) was used to:
  - Convert all Boltz2 output `.cif` files to `.pdb` format
  - Consolidate all resulting PDBs into a single directory (`all_pdbs/`)
- This standardized directory structure simplifies downstream affinity prediction analysis.

---

## 5. PPI-Graphomer Batch Affinity Prediction

- PPI-Graphomer was configured for batch affinity prediction using the consolidated PDB directory.
- One preprocessing script (generate_batch.py) in the PPI-Graphomer codebase was modified because:
  - The original implementation assumed the presence of ground-truth affinity values
  - This project performs inference only, without experimental labels
  - Original (line 80):
    `affinity.append(torch.tensor(item["affinity"]))`
  - New version:
    `val = item.get("affinity", None)
    if val is None:
        val = float("nan")   # placeholder for unlabeled prediction
    affinity.append(torch.tensor(val, dtype=torch.float32))`
  - Otherwise, all PPI-Graphomer installation and use instructions were followed exactly as listed on their GitHub. 
  - Note: PPI-Graphomer is a third-party repo and is not committed here. To reproduce, clone PPI-Graphomer separately and apply the patch (patches/ppi-graphomer_inference_only.patch)

---

## 6. Rosetta InterfaceAnalyzer Scoring

- Rosetta InterfaceAnalyzer was used as an alternative method for interface evaluation (see setup in rosetta_InterfaceAnalyzer/interfaceanalyzer.sb).
- Selected interface metrics were extracted from Rosetta score files for comparison using get_scores.py.

---

## 7. Score Consolidation

- Final results from PPI-Graphomer and Rosetta InterfaceAnalyzer were compared:
    - PPI-Graphomer: ppi-graphomer/result/default/evaluate.csv
    - Rosetta InterfaceAnalyzer: rosetta_InterfaceAnalyzer/selected_rosetta_scores.csv

---

## Notes

- This repository is intended to document how the tools were set up and connected, not to evaluate or benchmark their performance.
- No experimental affinity data are used.
- Results and conclusions are intentionally excluded from this README.