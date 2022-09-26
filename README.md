# pyFAVA

A python interface to the Fermi All-sky Variability Analysis data portal

https://fermi.gsfc.nasa.gov/ssc/data/access/lat/FAVA

## Installation

### Requirements

- Python >= 3.5
- numpy >= 1.17.3
- urllib.request >= '3.10'
- json >= '2.0.9'

### How to Install

Installing the script from the command line

`git clone https://github.com/dankocevski/pyFAVA`

## Usage

Downloading the FAVA data from a single week

`data = pyFAVA.getWeeklySources(week=1, threshold=6)`

Downloading the FAVA data from all the availble weeks

`data = pyFAVA.downloadCatalog(start_week=1, end_week=721, threshold=6)`

Selecting a subset of data in the galactic plane

`galacticData = pyFAVA.selectGalacticSources(data, dgalb=10)`

