---
output:
  word_document: default
  html_document: default
  pdf_document: default
---

# Climate Projections Viewer

## Final Project for the Alfatraining Python Course

### Author: Dr. Fernando Moyano

### Instructor: Dr. Christoph Feiler

---

### General Objectives

Create a graphical user interface (GUI) that allows downloading projected future climate data, taking into account a range of choices, including region, time, variable and future scenario. Data summaries, statistics and visualizations should then be performed.

### GUI options and functions

Data retrieval and loading:

* Open a local .nc file
* Download data with options:
  * climate variable
  * time range
  * region coordinates
  * frequency (time steps daily or monthly)
  * todo: emission scenario (weaker or stronger global warming)

Data summaries:

* statistic:
  * temperal and spatial means and variance
  * temporal trends
  * max, min values
  
* descriptors:
  * variable name
  * .nc file variable name
  * region coordinates
  * time range

Visualization:

* time line plots:
  * averaged over region
  * todo: plot multiple time series
  
* regional maps plots:
  * averaged over time range

Data manipulation

* todo: subset data by choosing new time or coordinates

Files functions:

* save summary key value pairs as .json file
* save dataset as .csv file

## Code description

### Main Functions

make_gui()

* Creates the main interface window
* Defines functions:
  * b1_open_file(): loads a .nc file
  * b6_plotmap(): creates map plot
  * b5_plottime(): creates the line plot
  * other minor functions

get_dsdata()

* Extracts data from the loaded .nc file and writes it into a global variable (ds_vars).

getdata_gui()

* Creates a window for configuring a data download request (see Data Source below)
* Calls the getdata() function
* Can be run independently from main.py

getdata()

* Uses configured options to generate a data download request

getstats()

* calculates summary statistics and describes units, bounds, etc.

  
### Data source

Data source:
http://cds.climate.copernicus.eu/
cmip6 climate projections data

Requires:
- python library: cdsapi
- Follow instruction at: https://cds.climate.copernicus.eu/api-how-to

### ToDo

- [ ] Add scenarios
- [ ] Documentation: in code, help
- [ ] Add time span to summary
- [ ] Add trendline to plot and to stats
- [ ] Add coordinates to dir name
- [ ] Make maps stick to windows border
- [ ] Option: save data as .csv
- [ ] Option: subset active dataset
- [ ] Option: save summary as .json
- [ ] Add yes/no dialogue with size estimate message before download
- [ ] Add Class code
- [ ] Improve plots
- [ ] Allow loading of multiple datasets and simultaneous plotting
- [ ] Convert time to time variable: insures proper axis units and is better readable.
- [ ] Add a help menu/button that displays an explanation text
- [ ] Use validate for input fields: Check kap_19_tkinter_validate1 for callback functions validating inputs




