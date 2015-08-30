# Flood Commander
Batch processing of data for the calculation of floodlines.

###1. Introduction

This project consists of a collection of scripts that aids an engineer with the 
determination of floodlines.

###2. Documentation

Under the notebook folder is an *IPython/Jupyter Notebook* indicating and documenting a step by step example project for flood line determination.

###3. Target Audience

My target audience will be primarily engineers with very little or no programming experience.

###4. Installation

For now the project can just be cloned or downloaded and run from a Python 3 environment. My recommendation for getting started in Python is to download the [Anaconda](http://continuum.io/downloads) distribution. Make sure you download Python 3.4

###5. Dependencies

* [Fiona](http://toblerity.org/fiona/) (`conda install fiona`)
* [SAGA](http://www.saga-gis.org/en/index.html)  
    SAGA is used to generate the grid DTM and to calculate the exact floodline. I am not using the Python interface but rather the command line interface.

###6. Input Data Required

All the input data is in the ESRI Shapefile format:

* Contours and/or point heights
* River or stream centre line(s)
* Cross sections

###7. Output

* An **.sdf* file to be used as input to [HEC-RAS](http://www.hec.usace.army.mil/software/hec-ras/).

###8. Post-processing

The simulation results exported from [HEC-RAS](http://www.hec.usace.army.mil/software/hec-ras/) is processed to produce the resulting floodline as a shapefile, a DXF file and a PNG.

###9. Todo

* Cross section simplification (Can be done within HEC-RAS for now anyway)
* Input data validation
* Support for [FEQ](http://il.water.usgs.gov/proj/feq/)

###10. Similar Projects

* [RiverGIS](https://github.com/erpas/rivergis)
* [pyras](https://github.com/PyHydro/pyras)
* [Giswater](https://github.com/Giswater/giswater)

