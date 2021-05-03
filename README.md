# Analysis and Visualization of Projected Climate Data


## Final Project for the Alfa Training Python Course


### General Objectives

Create a Python program that creates a GUI through which a user can select future projected climate data for a location [or region?] and obtain various statistics and visualizations.

### GUI options and functions

User can select: 

* [choose data source. Local data files vs online (e.g. based on climate model)]
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

Gett from 

* Coordinates for Germany (rounded): 47N-55N and 6E-15E
* Coordinates for Córdoba (rounded): 29S-35S and 62W to 66W

### 