# SNe-heated_Gas_Flow
Python code and analysis of Justice League simulation -- analyzing the effect of SN on gas flows

---
#### Author: Mitsuru Watanabe

#### Adviser: Professor Charlotte Christensen

#### Grinnell College, IA

#### Summer 2023 

---

This word is a continuation of past students at Grinnell College, namely Hollis Akins and Leo Lonzarich. Their past work can be found via https://github.com/hollisakins/Justice_League_Code.git for Hollis' and https://github.com/leoglonz/Stellar_Feedback_Analysis.git for Leo's. <par>

This repository is structured in three sections: base code, script files, and Jupyter notebooks. Base code includes repetitive functions necessary in computing and analyzing data, scripts include computing and outputting data, and notebooks include analysis and plotting. <par>

## Basic Code
* `base.py`
* `analysis.py` (not actively used in this repo)
* `compiler.py`

## Scripts
* `rampressure.py`
* `particletracking.py`
* `write_discharged.py`

## Notebooks
* `particletrackingpractice.ipynb`
* `stellarfeedbackanalysis.ipynb`

## Data
All gas particles treated in this research are sourced from 28 satellites in DC Justice League cosmological simulation data, chosen since they have virial stellar masses above 2e7 Msol, either quenched or star-forming at z = 0, listed as follows:
* h148 (Sandra)
** 3, 4, 6, 10, 12, 27, 34, 38, 55, 65, 249, 251, 282
* h229 (Ruth)
** 14, 18, 20, 22, 49
* h242 (Sonia)
** 10, 21, 30, 38
* h329 (Elena)
** 7, 29, 117

## Github
My GitHub repository is based in https://github.com/avocado-mw/SNe-heated_Gas_Flow.
Most of the python codes and scripts, as well as Jupyter notebooks are inherited from Leo’s and Hollis’s. To see some larger files (ex. hdf5), you can head to watanabe@quirm.math.grinnell.edu/watanabe_MAP/SNe-heated_Gas_Flow. \n