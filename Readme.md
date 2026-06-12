## PHD - Chapter 5 - Chapter 5. Flower visitation duration as a metric for characterising plant-pollinator interactions using computer vision-derived data

This repository contains data analysis and supporting materials for chapter 5 of my thesis. 

The chapter has the following aims which the analysis looks to address:
1.	evaluate variables influencing the duration of visitation events to assess its potential as a proxy for pollinator foraging success,
2.	explore visitation dynamics across individual flowers,
3.	analyse the relationship between time spent at a flower and the time elapsed since previous visitations, and
4.	assess intra- and interspecific pollinator competition, using flower visitation duration as a proxy for visit success.

## Contents

'Chapter5.ipynb': Main analysis contents in jupyter notebook

'RScripts/': R scripts that were run as part of the analysis (due to limitations of python for some analysis)

'results/': Folder with results of R script analysis. Results for the jupyternotebook are displayed within the notebook. However, these outputs are also displayed in the notebook

'plot_outputs/': output graphs from analysis

## Requirements

Python 3.x
Python module requirements in the requirements.txt file (pip install -r requirements.txt)
R module requirements: mgcv, lme4, lmerTest, MuMIn

## Advice on how to run 

Jupyter notebook must be installed. Best to run using a virtual environment that is linked with the notebook. How to do this is shown below:

pip install virtualenv 
virtualenv ch5
source ch5/bin/activate
pip install -r requirements.txt
python3 -m ipykernel install --user --name=ch5 --display-name="Chapter5"

Then in your jupyter notebook, under kernel (top right) select Chapter5

