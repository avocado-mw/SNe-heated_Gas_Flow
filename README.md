# SNe-heated_Gas_Flow
Python code and analysis of Justice League simulation -- analyzing the effect of SN on gas outflows

---
#### Author: Mitsuru Watanabe

#### Adviser: Professor Charlotte Christensen

#### Grinnell College, IA

#### Summer 2023 - Spring 2024

---

## Project Description
This project is a continuation of past students at Grinnell College, namely Hollis Akins and Leo Lonzarich. Their past work can be found via https://github.com/hollisakins/Justice_League_Code.git for Hollis' and https://github.com/leoglonz/Stellar_Feedback_Analysis.git for Leo's.
    
The research was conducted to answer the questions of the following:
- How does the mass of the satellite affect the role of SN in gas loss
- How does changing SFR around infall affect the SN-driven gas outflow for different mass sizes of the galaxies
- Why the mass loading factor is similar before and after infall. How does this relate to mass sizes of the galaxies
- Of the gas that are heated by SNe, what fraction of the gas is lost from the satellite
- Is there any angle dependency on discharged gas? If any dependent on angles, how in different times in infall, and from which the gas is discharged, the role of ram pressure stripping varies??


## Directory
This repository is structured in the following diagram.

.
├── codes                   
│    ├── base code          # repetitive functions (.py)
│    ├── scripts            # functions used in a notebook (.py)
│    └── notebooks          # analysis codes and plots (.ipynb)
├── archiveData             # archive of hdf5 files (.hdf5)
├── logs                    # archive of tracking log (.log)
├── plots                   # plot storage (.pdf, .png)
├── SNeData                 # file storage (.csv, .hdf5, .data)
└── README.md

Base code includes repetitive functions necessary in computing and analyzing data, scripts include computing and outputting data, and notebooks include analysis and plotting.

    
## Basic Code
* `base.py`
* `analysis.py` (not actively used in this repo)
* `compiler.py`
Major contributions include the redefinition of expelled gas, and all gas that are SN-heated. Most of the functions are inherited from past researchers.


## Scripts
* `particletracking.py`
Tracks particles within satellites. Use `runall.sh` to run for all satellites.
* `write_discharged.py`
Compiles discharged gas particles into data set.
* `infallinganalysis.py`
Calculates the distance and SFR over time, and mass loading factor.
* `dischargedgastracking.py`
Calculates the energy of discharged particle.

    
## Notebooks
Notebooks are separated based on the kinds of research questions addressing and the time in the semester the research is conducted. Each notebook has a header explaining the main research question and key findings, and often mentions other parts of the notebook assembly following before or after. Most notebooks require `base.py`, `analyzer.py`, `compiler.py` to be compiled. Some require its child `.py` file as well. All require the connection to quirm which stores tracked particles data frame.

* `particletrackingpractice.ipynb`
Produces 3 plots: particletracking, particletracking_advanced, and fraction data.
* `rampressurepractice.ipynb`
Had troubles with the advanced technique Hollis used for calculating the ram pressure, so I halted my analysis.
* `stellarfeedbackanalysis.ipynb`
Requires `write_discharged.py` to run first (probably should sign in to quirm to do these). Inherited from Leo’s python code. 
* `infallinganalysis.ipynb`
Analyzes the relationship b/w SFH and infalling types on SN-heated gas loss and how mass loading factor or fraction of gas loss changes with respect to mass and time. Requires `infallinganalysis.py` to be compiled. This work is followed by `F23_SNe_Gas_Loss.ipynb`.
* `dischargedgastracking.ipynb`
Traces the discharged gas particles over different snapshots and figure out the relation to SN-heating, as well as calculating the energy that discharged gas particles have when exitted, requires `dischargedgastracking.py` to be compiled.
* `snheating.ipynb`
Traces the fraction of gas loss due to supernovae over time. I found that the ram pressure does boost the expulsion of the gas both discharged and expelled, confirming the result from infalling analysis. This is a follow-up from `dischargedgastracking.ipynb`. 
* `F23_Plotting.ipynb`
Plots the infall trajectory of each individual galaxy as well as the corresponding gas loss and star formation rate.
* `F23_SNe_Gas_Loss.ipynb`
Computes and plots the fraction of SN-driven outflow and the fraction of perimanent gas loss at different times in infall, namely at 1 virial radius away or at 1st pericentric passage.
* `S24_ExitAngleOverTime.ipynb`
Analyzes the relationship between the launched angle of discharged gas and the time it discharged or the stellar mass of the galaxy from which the gas is discharged.


## Data
Original data should be stored under `SNedata` folder. This can originally be accessed through quirm->watanabe->watanabe_MAP->SNe-heated_Gas_Flow.

Currently, tracked_particles and rampressure hdf5 files are stored under Justice League code. And discharged, predischarged, expelled, and accreted particles hdf5 files are stored under SNedata folder (quirm access required). Expelled particles are recalculated from Leo's.
    
During the process of analysis, I used averaged mass loading factor, fraction of gas loss, and SFR over different times of infall, such as before and after infall, around 1st pericentric passage, before and after reaching 1 Rvir from the host. Those information (avg values) is saved on `all-satellite-information2.csv` file under SNeData. It is used to divide the discharged gas into small chunks, based on a certain time at infall.

All gas particles treated in this research are sourced from 28 satellites in DC Justice League cosmological simulation data, chosen based on stellar masses ranging from $10^6$ to $10^8 M_{sol}$ approximately, either quenched or star-forming at z = 0, and followed by the analysis of Hollis et al. in prep listed as follows ('h242_401' is tracked but always excluded in the analysis):
* h148 (Sandra)
    - 2, 3, 4, 6, 10, 12, 27, 34, 38, 55, 65, 249, 251, 282
* h229 (Ruth)
    - 14, 18, 20, 22, 49
* h242 (Sonia)
    - 8, 10, 21, 30, 38, 69
* h329 (Elena)
    - 7, 29, 117

**Other files stored under quirm**
* `all-satellite-data-overtime.csv`
Last snapshot of each galaxy with information, from Akin's. Used in `infalling analysis.ipynb`.
* `avg_mlf_calculation.csv`
Average MLF calculation used in `infalling analysis.ipynb`.

    
## Key Terms
Discharged gas are gas particles that have been removed from the disk of their respective satellite galaxy to the halo. For each unique gas particle ID, I look at the `coolontime` and compare with the time 1 timestep before. The gas is SN-heated if the coolontime is larger than time before (functionally, their 'cooling' was turned off). Note that this dataset can be also be obtained by selecting particles from *discharged* with `sneHeated==True`.

Expelled gas are gas particles that are permanently discharged. It is a subset of discharged gas, either discharged only once and never be accreted after or once reaccreted then discharged again permanently (at least by z=0). SN-heated expelled gas can be found through setting the property `sneHeated==True`.

Accreted gas are particles in the halo or beyond the virial radius of a satellite that are accreted onto the satellite's disk. Those gas can be reaccreted if the gas once discharged then be accreted. The reaccretion might happen multiple times and it is a subset of accreted gas. 

Predischarged/expelled gas are discharged/expelled gas one step before being discharged/expelled. It is the same particles in discharged/expelled gas dataset, but instead giving the properties of each particle prior to their discharge event (thereby allowing pre- and post-discharge comparisons).


## Acknowledgment
Most of the python codes and scripts, as well as Jupyter notebooks are inherited from Leo’s and Hollis’s. I would like to thank Professor Charlotte Christensen, and past researchers for their support.
