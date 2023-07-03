# Tackling the Energy Cost of High Energy Physics

## Introduction
This repository contains the code for the summer project titled "Tackling the Energy Cost of High Energy Physics," supervised by Prof Caterina Doglioni. The project aims to address the energy consumption challenges in high-energy physics.

## Code Description

The code in this repository is based on the following components:

1. **antikt-python**: This codebase, developed by Graeme A. Stewart, is available at [https://github.com/graeme-a-stewart/antikt-python](https://github.com/graeme-a-stewart/antikt-python). It provides the necessary tools for generating Pythia events.

2. **rivet jet analysis**: The base rivet analysis code utilized in this project was provided by Dr. Sukanya Sinha (The University of Manchester).


## Dataset
For comparison purposes, this project employs Graeme Stewart's original dataset. The dataset used for analysis can be accessed from the following location: [link to Graeme's original dataset](https://github.com/graeme-a-stewart/antikt-python/tree/main/data).

## Prerequisites
To run this project, you need to have the `hepstore/rivet-pythia` Singularity container installed on your system. This container provides the required environment for executing the code.

To install Singularity and the `hepstore/rivet-pythia` container, please follow the instructions provided in their respective documentation:

- Singularity: [https://sylabs.io/guides/3.7/user-guide/](https://sylabs.io/guides/3.7/user-guide/)
- hepstore/rivet-pythia container: [https://hub.docker.com/r/hepstore/rivet-pythia)

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/software-energy-cost-studies/jet-algorithm-studies.git
2. Enter this directory:
   ```bash
   cd summer-project
3. Start the `hepstore/rivet-pythia` Singularity container:
   ```bash
   singularity run rivet-pythia*.sif

## Usage
Detailed instructions on how to use the code can be found in the respective repositories mentioned above. Ensure that the `hepstore/rivet-pythia` Singularity container is running before executing the code.

To install use:
   ```bash
   singularity pull docker://hepstore/rivet-pythia
   ```

To generate events:
1. Compile the `generator.cc` programme:
   ```bash
   g++ -o generate-events generator.cc -L./pythia/include -lpythia8 -lHepMC3
2. Run the programme:
   ```bash
   ./generate-events
This will generate a new file named `events.hepmc3`.

To use the analysis code:
1. Compile using rivet:
   ```bash
   rivet-build ptanalyser.cc
2. Run the analysis `PtPlot`:
   ```bash
   rivet -a PtPlot --pwd <file name to be analysed>

---
## For the Final Analysis only
To generate multiple events files from 13TeV to 100TeV:
1. Compile the multi_generator(_parallel).cc where parallel is for multi-threaded compilation:
   ```bash
   g++ -o multi-generator(-parallel) multi_generator(_parallel).cc -L./pythia/include -lpythia8 -lHepMC3 (-fopenmp)
   ```
remove the **()** before running. <br />
2. Run the generator
   ```bash
   ./multi-generator(-parallel)
   ```
**Tip**: The files will be around 100+ GB. Store them in a storage space which will be enough. If running on lxplus, ensure storage is on EOSBox.
---

To generate comparing plots:
1. Rename the yoda files for the original events from Graeme to `OriginalData.yoda`, and then re-run the analysis on the generated dataset. 
2. Based on the analysis used, the `plotting.py` file will need to be changed to reflect the proper histogram name.
3. Run the plotter using:
   ```bash
   python3 plotting.py

Please note that the commands provided assume a Unix-like environment. Make sure you have the necessary dependencies installed for successful compilation and execution.
