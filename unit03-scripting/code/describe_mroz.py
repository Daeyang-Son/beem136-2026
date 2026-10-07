"""
describe_mroz.py
Descriptive statistics and a wage regression for Mroz (1987).
Input:  data/mroz.csv
Output: output/table1_means.csv, output/table2_wage.txt
Run from the project root with:  python code/describe_mroz.py
"""
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf

# ---- 1. Paths -------------------------------------------------------------
DATA = Path("data")
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

# ---- 2. Load and check ----------------------------------------------------
mroz = pd.read_csv(DATA / "mroz.csv")
assert mroz.shape == (753, 22), "Unexpected size: has the raw file changed?"
assert mroz["inlf"].isin([0, 1]).all()
# wages should be observed for exactly the women in the labour force
assert (mroz["wage"].notna() == (mroz["inlf"] == 1)).all()

# ---- 3. Construct variables -----------------------------------------------
mroz["young_kids"] = (mroz["kidslt6"] > 0).astype(int)
mroz["college"] = (mroz["educ"] >= 16).astype(int)

# ---- 4. Descriptive table -------------------------------------------------
cols = ["age", "educ", "young_kids", "college", "wage"]
table1 = mroz.groupby("inlf")[cols].mean().T.round(3)
table1.to_csv(OUTPUT / "table1_means.csv")

# ---- 5. Regression --------------------------------------------------------
workers = mroz[mroz["inlf"] == 1]
res = smf.ols("lwage ~ educ + exper + expersq", data=workers).fit(cov_type="HC1")
(OUTPUT / "table2_wage.txt").write_text(res.summary().as_text())

print(table1)
print(f"Return to a year of education: {res.params['educ']:.3f}")
