# OER-ML-paper

Machine learning applied to quaternary noble-metal alloy electrocatalysts for the
oxygen evolution reaction (OER).  Composition–property relationships are extracted
from high-throughput cyclic voltammetry data and used to train predictive models
for three electrochemical descriptors: Tafel slope, overpotential at 10 mA/cm²
(η₁₀), and the full shape of the differential Tafel curve (dJ/dV).

## Background

The dataset was generated with a custom high-throughput Single Droplet Cell
(HT-SDC) using 0.5 mL of 0.1 M H₂SO₄ electrolyte.  Cyclic voltammetry (CV) was
recorded for a combinatorial library of {Ir, Pt, Au, Pd} quaternary alloys; only
the 5th forward scan is used for analysis to ensure steady-state conditions.

## Repository structure

```
.
├── CV.zip                   Raw CV data files (one .csv per sample)
├── dJdV/                    Preprocessed dJ/dV curves (output of preprocessing.ipynb)
├── djdVgraphs/              Per-sample dJ/dV fit plots (output of dJdVpreprocess.ipynb)
├── PtPdAuIr_summary.csv     Composition and iR-drop lookup table
├── composition_Tafel.csv    Composition + Tafel slope (output of preprocessing.ipynb)
├── composition_eta.csv      Composition + η₁₀ (output of preprocessing.ipynb)
├── composition_djdV.csv     Composition + dJ/dV fit params (output of dJdVpreprocess.ipynb)
├── preprocessing.ipynb      ① Tafel slope + η₁₀ extraction from raw CV
├── dJdVpreprocess.ipynb     ② dJ/dV curve fitting (logistic + Gaussian model)
├── ml_tafel.ipynb           ③ ML: predict Tafel slope from composition
├── eta_prediction.ipynb     ④ ML: predict η₁₀ from composition
├── ml_djdv.ipynb            ⑤ ML: predict dJ/dV parameters from composition
└── oer_research.yml         Conda environment specification
```

## Installation

```bash
conda env create -f oer_research.yml
conda activate oer_research
```

Python 3.12 is required.  All dependencies are pinned in the `.yml` file.

## Usage

Run the notebooks in order; each one produces output files consumed by the next.

| # | Notebook | Inputs | Outputs |
|---|----------|--------|---------|
| ① | `preprocessing.ipynb` | `CV.zip`, `PtPdAuIr_summary.csv` | `composition_Tafel.csv`, `composition_eta.csv`, `dJdV/` |
| ② | `dJdVpreprocess.ipynb` | `dJdV/`, `PtPdAuIr_summary.csv` | `composition_djdV.csv`, `djdVgraphs/` |
| ③ | `ml_tafel.ipynb` | `composition_Tafel.csv` | `feature_importance.png`, `shap_dependence_plot_Ir.png` |
| ④ | `eta_prediction.ipynb` | `composition_eta.csv` | `parity_plots.png`, `feature_importance_eta.png` |
| ⑤ | `ml_djdv.ipynb` | `composition_djdV.csv` | `quaternary_*.pdf` |

### Electrochemical conventions

- **iR correction**: applied voltage is corrected as V_corr = V_meas − I·R, where R
  is the measured electrolyte resistance.
- **Overpotential**: η = V_corr − V_eq, with V_eq = 1.2891 V vs RHE (OER equilibrium
  potential in 0.1 M H₂SO₄, from the Nernst equation).
- **Tafel slope**: linear fit of η vs log₁₀(J) in the kinetically controlled region
  (−5 ≤ log₁₀(J) ≤ −2), reported in V/decade.
- **η₁₀**: overpotential interpolated at J = 10 mA/cm², the standard benchmarking
  current density for OER catalysts.

## License

MIT
