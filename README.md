# OER-ML-paper

Machine learning applied to quaternary noble-metal alloy electrocatalysts for the
oxygen evolution reaction (OER).  Composition–property relationships are extracted
from high-throughput cyclic voltammetry data and used to train predictive models
for overpotential (η₅), apparent Tafel slope, the full shape of the differential
Tafel curve (dJ/dV), and durability under an etching hold.

## Background

The dataset was generated with a custom high-throughput Scanning Electrochemical Cell
(HT-SEC) using 0.5 mL of 0.1 M H₂SO₄ electrolyte.  Cyclic voltammetry was recorded
for a combinatorial library of {Ir, Pt, Au, Pd} quaternary alloys at 50 mV/s over
0 → 1.9 V vs Ag/AgCl, five cycles per spot.  Durability data from a separate 3 h
chronoamperometry hold is provided in `data/external/`.

### Which part of the scan is used

Analysis runs on the **5th cycle**, and within it on the **reverse (cathodic-going)
sweep**.  On the forward sweep the oxide-formation wave folds the η–log J curve back
on itself so that it fails the vertical line test; on the reverse sweep the surface
is already oxidized and the OER branch is single-valued and quasi-linear.

The one exception is dJ/dV, which is built from the **average of both sweeps**,
½·(J_fwd + J_rev).  Capacitive current is +C·ν on the forward sweep and −C·ν on the
reverse, so averaging cancels it, and cancels the reversible surface redox with it.
η₅, η₁₀, the Tafel slope and the background all stay on the reverse sweep alone,
where averaging would fold the forward oxide wave back in.

## Repository structure

```
.
├── data/
│   ├── CV.zip                     Raw CV data (one .csv per spot); unzipped to data/CV/ on first run
│   ├── PtPdAuIr_summary.csv       Composition, wafer position and iR-drop lookup table
│   ├── dJdV/                      Faradaic dJ/dV curves (output of preprocessing.ipynb)
│   ├── composition_Tafel.csv      Composition + Tafel slope, C_dl, background
│   ├── composition_eta.csv        Composition + η₁₀ and η₅
│   ├── composition_djdV.csv       Composition + dJ/dV fit parameters
│   ├── composition_durability.csv Composition + per-element mass change
│   └── external/                  Corrosion spreadsheet (durability source data)
├── images/
│   ├── CV/                        Cycle 5 forward + reverse with the double-layer gap
│   ├── Tafel/                     Journal-style Tafel plot per spot
│   ├── TafelDiagnostics/          Branch, fit window and fitted line per spot
│   └── djdVgraphs/                Per-spot dJ/dV fit plots
├── oer_utils.py                   Shared data-loading and composition-matching helpers
├── djdv_model.py                  Shared dJ/dV curve model (sigmoid + Gaussian)
├── preprocessing.ipynb            ① Tafel slope, η, C_dl and dJ/dV curves from raw CV
├── dJdVpreprocess.ipynb           ② dJ/dV curve fitting
├── corrosion_preprocess.ipynb     ③ Durability targets from the corrosion spreadsheet
├── ml_tafel.ipynb                 ④ ML: apparent Tafel slope from composition
├── eta_prediction.ipynb           ⑤ ML: η₅ from composition
├── ml_djdv.ipynb                  ⑥ ML: dJ/dV curve parameters from composition
├── ml_durability.ipynb            ⑦ Durability analysis
└── oer_research.yml               Conda environment specification
```

## Installation

```bash
conda env create -f oer_research.yml
conda activate oer_research
```

Python 3.12 is required.  The `.yml` file lists the direct dependencies and
resolves the rest through conda-forge.

## Usage

Notebooks ① and ③ write the CSVs the rest consume, so run them first.  ② depends on
① and must follow it.  ④–⑦ read only CSVs and can be run in any order once their
inputs exist.

| # | Notebook | Inputs | Outputs |
|---|----------|--------|---------|
| ① | `preprocessing.ipynb` | `data/CV.zip`, `data/PtPdAuIr_summary.csv` | `data/composition_Tafel.csv`, `data/composition_eta.csv`, `data/dJdV/`, `images/CV/`, `images/Tafel/`, `images/TafelDiagnostics/` |
| ② | `dJdVpreprocess.ipynb` | `data/dJdV/`, `data/PtPdAuIr_summary.csv` | `data/composition_djdV.csv`, `images/djdVgraphs/` |
| ③ | `corrosion_preprocess.ipynb` | `data/external/corrosion.xlsx` | `data/composition_durability.csv` |
| ④ | `ml_tafel.ipynb` | `data/composition_Tafel.csv` | `images/tafel_parity.png`, `images/feature_importance.png`, `images/shap_*.png` |
| ⑤ | `eta_prediction.ipynb` | `data/composition_eta.csv`, `data/composition_Tafel.csv` | `images/parity_plots.png`, `images/eta_censoring_diagnostic.png` |
| ⑥ | `ml_djdv.ipynb` | `data/composition_djdV.csv`, `data/dJdV/`, `data/PtPdAuIr_summary.csv` | `images/djdv_curve_gallery.png`, `images/quaternary_*.pdf` |
| ⑦ | `ml_durability.ipynb` | `data/composition_durability.csv`, `data/external/corrosion.xlsx` | `images/durability_*.png` |

Re-running ① regenerates `data/dJdV/`, so ② must be re-run after it.

## Electrochemical conventions

- **iR correction**: η = V + E_ref/RHE − I·R − 1.23, with R the per-spot EIS
  resistance from `PtPdAuIr_summary.csv`.  Applied to η₅, η₁₀ and the Tafel slope.
  The dJ/dV curves are kept on the raw applied-potential axis.
- **Reference scale**: potentials are logged against Ag/AgCl;
  E_ref/RHE = 0.197 + 0.0592·pH ≈ +0.256 V in 0.1 M H₂SO₄.  A non-saturated filling
  solution would shift every η by 8–13 mV.
- **η₅ and η₁₀**: overpotential at J = 5 and 10 mA/cm².  η₅ is the modelling target;
  16 spots never reach 10 mA/cm² within the 1.9 V scan window, and those spots are
  not missing at random (they are low-Ir and concentrated in one deposition run), so
  training on η₁₀ would drop a specific corner of the composition space.
- **Tafel slope**: least-squares fit of η vs log₁₀(J) over a common
  1.0–5.5 mA/cm² window.  This is an *apparent* slope at 50 mV/s rather than a
  steady-state kinetic parameter; forward and reverse branches sit 130–160 mV apart
  at matched current density, comparable to the 139 mV the window spans.  It is
  computed identically for every spot and is valid for ranking within this library.
- **C_dl**: from the forward/reverse gap in the 0.30–0.50 V vs Ref window,
  C_dl = ΔJ / (2ν).  Reported as measured and not converted to a surface area: the
  scans reach 1.9 V vs Ref on every cycle, which grows hydrous oxide, and the charge
  stored there is pseudocapacitive rather than double-layer.

## Evaluation

Each deposition run is a composition-spread wafer, so neighbouring spots have nearly
identical compositions and share a sputter session, substrate and reference
electrode.  A random train/test split therefore puts near-duplicate spots on both
sides of the partition and measures interpolation rather than prediction.  All three
composition-to-property notebooks report **leave-one-run-out** cross-validation
alongside random CV; the gap between them measures how much apparent skill is
run-specific.  `ml_durability.ipynb` has one row per run (n = 6) and uses
leave-one-out with a permutation null.

## License

MIT
