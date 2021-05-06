# Analysis and Visualization of Projected Climate Data


## Final Project for the Alfa Training Python Course


### General Objectives

Create a graphical user interface (GUI) that allows downloading future projected climate data, taking into account a range of choices, including region, time, variable and future scenario. Various statistics and visualizations shoudl then be performed on the data.

### GUI options and functions

Data retrieval and loading

* Open a local .nc file
* Download data [choose data source. Local data files vs online (e.g. based on climate model)]
* variable: surface temperature, precipitation, max/min temp [, other?]
* time range [somewhere between present to 2100]
* statistic to show

Output includes:

* single statistics displayed in a window
* time line plots
* [regional maps plots]
* .json files as key value pairs
* .csv files with time series outputs
* [Side by side plot comparison]


### Main internal functions

* [get netcdf from internet]
* read in data from netcdf file (needs: lat, lon, start date, end date)
* [interpolate for single point?]  
* calculate overall statistics
* calculate yearly statistics
* plot time series
* [plot map]
* save to .json
* save to .csv
* make GUI:
    * Help menu/button
    * Load netcdf file
    * Loaded data info
    * Calculate overall statistics
    * Calculate yearly statistics
    * Plot time series
    * [Plot map]
    * plot side by side
        * options: share axes, ...
  
### The data

Data source:
http://cds.climate.copernicus.eu/
cmip6 climate projections data

Requires:
- python library: cdsapi
- Follow instruction at: https://cds.climate.copernicus.eu/api-how-to

---
Notes:
* Coordinates for Germany (rounded): 47N-55N and 6E-15E
* Coordinates for Córdoba (rounded): 29S-35S and 62W to 66W
---

### ToDo

- [ ] Add scenarios
- [ ] Documentation: in code, help
- [ ] Add time span to summary
- [ ] Add coordinates to dir name
- [ ] Make maps stick to windows border
- [ ] Option: save data as .csv
- [ ] Option: subset active dataset
- [ ] Option: save summary as .json
- [ ] Add yes/no dialogue with size estimate message before download
- [ ] Add Class code
- [ ] Improve plots
