import pandas as pd
import statsmodels.formula.api as smf

mroz = pd.read_csv("~/trabajo/Teaching/Exeter/ResearchMethods-I/2026/beem136-2026/unit03-scripting/data/mroz.csv")
workers = mroz[mroz["inlf"] == 1]
print(workers["wage"].describe())

model = smf.ols("lwage ~ educ + exper + expersq", data=workers)
results = model.fit(cov_type="HC1")
print(results.summary())
