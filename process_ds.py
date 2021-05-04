# Get inforamtion and variables form nc dataset
import itertools as it


def process_ds(ds):
    global ncvars
    global ncdims

    ncvars = list(ds.variables.keys())
    ncdims = list(ds.dimensions.keys())

    # Remove dim vars from var list
    isvar = [True] * len(ncvars)
    for v in range(len(ncvars)):
        for d in ncdims:
            if ncvars[v].find(d) != -1:
                isvar[v] = False
    ncvars = list(it.compress(ncvars, isvar))  # subset of variables

    # Get min and max values of dims (lat, lon)
    size_lat = ds.variables['lat'].size
    size_lon = ds.variables['lon'].size
    min_lat = ds.variables['lat'][0].data
    max_lat = ds.variables['lat'][size_lat - 1].data
    min_lon = ds.variables['lon'][0].data
    max_lon = ds.variables['lon'][size_lon - 1].data

    print(f"Variables in this file are: {str(ncvars).strip('[]')}")
    print(f"Dimensions in this file are: {str(ncdims).strip('[]')}")

