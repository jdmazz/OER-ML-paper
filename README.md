# Project Title: OER-ML-paper

This project uses machine learning (ML) to explore the relationships between quaternary alloy composition, linear sweep voltammetry (LSV), and the Tafel equations as a function of log(current density). This dataset was generated using a custom high-throughput Single Droplet Cell (HT-SDC) with 0.5 mL 0.1 M H2SO4 electrolyte solution. Cyclic voltammetry (CV) data for various alloy compositions of {Ir,Pt,Au,Pd} are recorded in the CV folder, but only the 5th forward cycle is used for analysis.

## Table of Contents
- [Installation](#installation)
- [Usage](#Usage)
- [License](#license)

## Installation
To install the necessary packages, use pip:
- pandas
- matplotlib
- scikit-learn
- seaborn
- shap

## Usage
- preprocessing.ipynb contains the Tafel plot generation from the raw CV data.
- ml_tafel.ipynb contains the {Ir,Pt,Au,Pd} features and Tafel slope ML code.

## License
MIT license
