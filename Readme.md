## Introduction

#### Setup

1. create and activate virtual environment

pip3 install virtualenv

virtualenv ch5

source ch5/bin/activate

2. download dependencies

pip install -r requirements.txt

3. Link environment to jupyter notebook

python -m ipykernel install --user --name=ch5 --display-name="Chapter5"

4. In Notebook, under kernel (top right) select Chapter5


## About Code

All code for chapter is in the Chapter5.ipynb file. 
Some Rscripts were used for statistical analysis (specifically LMM and GAM). These are in the RScripts folder. To run these, R must be installed and they must be Run using Rscript <file>.R.
Prerequisite libraries include: mgcv, lme4, lmerTest and MuMIn

Results from R analysis are saved to the results folder.

Graph outputs are plotted in the plot_outputs folder

