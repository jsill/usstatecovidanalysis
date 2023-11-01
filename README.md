# usstatecovidanalysis

This repository contains data, code and a working paper for the purposes of studying associations between the traits and policies of U.S. states and covid and excess death rates in the era prior to widespread vaccination (through May 2021).  The findings of my analysis are available within the pdf ( usStateCovidAnalysis.pdf ). The code for reproducing the results can be found in the notebook StateLevelCovidDeathAnalysis.ipynb. 

39 candidate variables which could be considered potential covariates for explaining U.S. state variation in covid death rates are contained in the spreadsheet us_states_covid_death_potential_covariates.csv. The variables include social distancing policy, socioeconomic factors, preexisting condition rates, climate, political leanings and other factors . The sources for the 39 variables are listed within the pdf. The code for extracting the variables from the original sources is in extractors.py.

The dataset builds upon a dataset constructed by Youyang Gu at https://github.com/youyanggu/covid19-datasets/blob/main/us\_states\_misc\_stats.csv.

