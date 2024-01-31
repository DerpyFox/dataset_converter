This repository converts data table from organism names and some features to data table with ftp links to download full genome and new added genome properties, with properties from original dataset.
After sorting, program excludes all copies, all .spp names, removes some errors in original names, removes all partial and contaminated genomes and removes all variables without any data about starting features.
Program was written with python and R. Example of dataset is in resourses folder. 

Information about scripts to edit master_.py.
First script have 1 variable -> name of original data table.
Second script have 3 variables -> first variable is generated from first script, second variable is type of data, "organism_name" or "taxid", recommended to use "taxid" for now, third variable is name for new generated table.
Third script have 2 variables -> first variable is generated from second script, second variable is name for new generated table.

Program needs to be executed from R enviroment.
https://docs.anaconda.com/free/anaconda/packages/using-r-language/

Needed libraries to execute:
Python: numpy, pandas, ete3.
R: data.table, httr, tidyverse, biomartr.
To install biomartr, check https://cran.r-project.org/web/packages/biomartr/readme/README.html, installation.

To execute run: python3 master_.py
