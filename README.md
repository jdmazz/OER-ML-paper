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
├── data/
│   ├── CV.zip                Raw CV data (one .csv per sample); unzipped to data/CV/ on first run
│   ├── PtPdAuIr_summary.csv  Composition and iR-drop lookup table
│   ├── dJdV/                 Preprocessed dJ/dV curves (output of preprocessing.ipynb)
│   ├── composition_Tafel.csv Composition + Tafel slope (output of preprocessing.ipynb)
│   ├── composition_eta.csv   Composition + η₁₀ (output of preprocessing.ipynb)
│   ├── composition_djdV.csv  Composition + dJ/dV fit params (output of dJdVpreprocess.ipynb)
│   └── external/             Corrosion-analysis data
├── images/                   All generated figures
│   └── djdVgraphs/           Per-sample dJ/dV fit plots (output of dJdVpreprocess.ipynb)
├── oer_utils.py              Shared data-loading and composition-matching helpers
├── djdv_model.py             Shared dJ/dV curve model (sigmoid + Gaussian)
├── preprocessing.ipynb       ① Tafel slope + η₁₀ extraction from raw CV
├── dJdVpreprocess.ipynb      ② dJ/dV curve fitting (logistic + Gaussian model)
├── ml_tafel.ipynb            ③ ML: predict Tafel slope from composition
├── eta_prediction.ipynb      ④ ML: predict η₁₀ from composition
├── ml_djdv.ipynb             ⑤ ML: predict dJ/dV parameters from composition
└── oer_research.yml          Conda environment specification
```

The notebooks import `oer_utils` and `djdv_model`, so launch Jupyter from the
repository root (where those files live) rather than from a subdirectory.

## Installation

```bash
conda env create -f oer_research.yml
conda activate oer_research
```

Python 3.12 is required.  The `.yml` file lists the direct dependencies and
resolves the rest through conda-forge.

## Usage

Run the notebooks in order; each one produces output files consumed by the next.

| # | Notebook | Inputs | Outputs |
|---|----------|--------|---------|
| ① | `preprocessing.ipynb` | `data/CV.zip`, `data/PtPdAuIr_summary.csv` | `data/composition_Tafel.csv`, `data/composition_eta.csv`, `data/dJdV/`, `images/tafel_plot_ex.png` |
| ② | `dJdVpreprocess.ipynb` | `data/dJdV/`, `data/PtPdAuIr_summary.csv` | `data/composition_djdV.csv`, `images/djdVgraphs/` |
| ③ | `ml_tafel.ipynb` | `data/composition_Tafel.csv` | `images/feature_importance.png`, `images/shap_dependence_plot_Ir.png` |
| ④ | `eta_prediction.ipynb` | `data/composition_eta.csv` | `images/parity_plots.png`, `images/feature_importance_eta.png` |
| ⑤ | `ml_djdv.ipynb` | `data/composition_djdV.csv` | `images/quaternary_*.pdf` |

### Electrochemical conventions

- **iR correction**: applied voltage is corrected as V_corr = V_meas − I·R, where R
  is the measured electrolyte resistance.
- **Overpotential**: η = V_corr − V_eq, with V_eq = 1.23 V vs RHE (standard OER
  equilibrium potential at 25 °C; on the RHE scale this value is pH-independent).
- **Tafel slope**: linear fit of η vs log₁₀(J) in the kinetically controlled region
  (−5 ≤ log₁₀(J) ≤ −2), reported in V/decade.
- **η₁₀**: overpotential interpolated at J = 10 mA/cm², the standard benchmarking
  current density for OER catalysts.

## License

MIT