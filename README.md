# SNe-heated_Gas_Flow
Python code and analysis of Justice League simulation -- analyzing the effect of SN on gas flows

---
#### Author: Mitsuru Watanabe

#### Adviser: Professor Charlotte Christensen

#### Grinnell College, IA

#### Summer 2023 

---

This word is a continuation of past students at Grinnell College, namely Hollis Akins and Leo Lonzarich. Their past work can be found via https://github.com/hollisakins/Justice_League_Code.git for Hollis' and https://github.com/leoglonz/Stellar_Feedback_Analysis.git for Leo's. <par>
    
The research was conducted to answer the questions of the following:
- How does the mass of the satellite affect the role of SN in gas loss
- How does changing SFR around infall affect the SN-driven gas outflow for different mass sizes of the galaxies
- Why the mass loading factor is similar before and after infall. How does this relate to mass sizes of the galaxies
- Of the gas that are heated by SNe, what fraction of the gas is lost from the satellite

This repository is structured in three sections: base code, script files, and Jupyter notebooks. Base code includes repetitive functions necessary in computing and analyzing data, scripts include computing and outputting data, and notebooks include analysis and plotting. <par>

    
## Basic Code
* `base.py`
* `analysis.py` (not actively used in this repo)
* `compiler.py`
Major contributions include the redefinition of expelled gas, and all gas that are SN-heated.

## Scripts
* `rampressure.py`
* `particletracking.py`
* `infallinganalysis.py`
Calculates the distance and SFR over time and outputs them together, as well as plotting mass loading factor (MLF) and its analysis
* `dischargedgastracking.py`
Calculates the energy at exiting of discharged particle, and calculates the all gas that are SN-heated (also in compiler.py)
* `write_discharged.py`

    
## Notebooks
* `particletrackingpractice.ipynb`
Produces 3 plots: particletracking, particletracking_advanced, and fraction data.
* `rampressurepractice.ipynb`
Had troubles with the advanced technique Hollis used for calculating the ram pressure, so I halted my analysis.
* `stellarfeedbackanalysis.ipynb`
Requires `write_discharged.py` to run first (probably should sign in to quirm to do these). Inherited from Leo’s python code. 
* `infallinganalysis.ipynb`
Analyzes the relationship b/w SFH and infalling types on SN-heated gas loss, requires `infallinganalysis.py` to be compiled.
* `dischargedgastracking.ipynb`
Traces the discharged gas particles over different snapshots and figure out the relation to SN-heating, as well as calculating the energy that discharged gas particles have when exitted, requires `dischargedgastracking.py` to be compiled.
* `snheating.ipynb`
Traces the fraction of gas loss due to supernovae over time. I found that the ram pressure does boost the expulsion of the gas both discharged and expelled, confirming the result from infalling analysis. 

     
## Data
Original data should be stored under SNedata folder. This can be accessed through quirm->watanabe->watanabe_MAP->SNe-heated_Gas_Flow. <par>
Currently, tracked_particles and rampressure hdf5 files are stored under Justice League code. And discharged, predischarged, and accreted particles hdf5 files are stored under SNedata folder (quirm access required). <par>
During the process of analysis, I used averaged mass loading factor, fraction of gas loss, and sSFR over different times of infall, such as before and after infall, around 1st pericentric passage, before and after reaching 1 Rvir from the host. Those information (avg values) is saved on all-satellite-information2.csv file under SNeData. <par>


All gas particles treated in this research are sourced from 28 satellites in DC Justice League cosmological simulation data, chosen based on stellar masses ranging from 10**6 to 10**8 approximately, either quenched or star-forming at z = 0, and followed by the analysis of Hollis et al. 2023, preplisted as follows:
* h148 (Sandra)
** 2, 3, 4, 6, 10, 12, 27, 34, 38, 55, 65, 249, 251, 282
* h229 (Ruth)
** 14, 18, 20, 22, 49
* h242 (Sonia)
** 10, 21, 30, 38
* h329 (Elena)
** 7, 29, 117

## Key Terms
Discharged gas are gas particles that have been removed from the disk of their respective satellite galaxy to the halo. For each unique gas particle ID, I look at the `coolontime` and compare with the time 1 timestep before. The gas is SN-heated if the coolontime is larger than time before (functionally, their 'cooling' was turned off). Note that this dataset can be also be obtained by selecting particles from *discharged* with `sneHeated==True`.<par>
Expelled gas are gas particles that are permanently discharged. It is a subset of discharged gas, either discharged only once and never be accreted after or once reaccreted then discharged again permanently (at least by z=0). Sn-heated expelled gas can be found through setting the property `sneHeated==True`.<par>
Accreted gas are particles in the halo or beyond the virial radius of a satellite that are accreted onto the satellite's disk. Those gas can be reaccreted if the gas once discharged then be accreted. The reaccretion might happen multiple times and it is a subset of accreted gas. <par>
Predischarged/expelled gas are discharged/expelled gas one step before being discharged/expelled. It is the same particles in discharged/expelled gas dataset, but instead giving the properties of each particle prior to their discharge event (thereby allowing pre- and post-discharge comparisons). <par>
All SN-heated gas particles are the ones that are sn-heated by comparing the coolontime 
with the time 1 timestep before. Since the detection of sn-heating doesn't depend on any positional argument,
this includes gas particles being SN-heated at any point. However, in order to avoid counting gas particles
that are outside the satellite, as those are likely not heated by the satellite, we should constrain only within the satellite.

## Github
My GitHub repository is based in https://github.com/avocado-mw/SNe-heated_Gas_Flow.
Most of the python codes and scripts, as well as Jupyter notebooks are inherited from Leo’s and Hollis’s. To see some larger files (ex. hdf5), you can head to watanabe@quirm.math.grinnell.edu/watanabe_MAP/SNe-heated_Gas_Flow. <par>
