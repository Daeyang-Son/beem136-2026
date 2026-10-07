import delimited "data/mroz.csv", clear
keep if inlf == 1
summarize wage

regress lwage educ exper expersq, robust
