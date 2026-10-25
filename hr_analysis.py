"""
IBM HR attrition: data checks and attrition rates by factor.

Usage:
    pip install pandas
    python hr_analysis.py

Put this file in the same folder as WA_Fn-UseC_-HR-Employee-Attrition.csv.
It prints the tables used in the README and saves each one as a CSV in an
"outputs" folder.

Note: written without access to your data file. If a column name differs,
the error message will name it; fix the name in the lists below.

Definition used everywhere:
    attrition rate = employees who left / all employees in that group
"""

import os
import pandas as pd

DATA_FILE = "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUT_DIR = "outputs"
MIN_GROUP = 30  # ignore groups smaller than this (too small to trust)

os.makedirs(OUT_DIR, exist_ok=True)
df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")  # utf-8-sig removes a hidden BOM
df["left"] = (df["Attrition"] == "Yes").astype(int)
overall = df["left"].mean()

# ---------------------------------------------------------------
# 1. DATA CHECKS
# ---------------------------------------------------------------
print(f"Rows: {len(df)}   Columns: {df.shape[1]}")
print("Total missing values:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
constant = [c for c in df.columns if df[c].nunique() == 1]
print("Columns with a single value (no information):", constant)
print("EmployeeNumber unique?", df["EmployeeNumber"].is_unique, "\n")

# ---------------------------------------------------------------
# 2. OVERALL ATTRITION
# ---------------------------------------------------------------
n_left = int(df["left"].sum())
print("OVERALL ATTRITION")
print(f"Employees: {len(df)}  Left: {n_left}  Stayed: {len(df) - n_left}")
print(f"Attrition rate: {overall * 100:.1f}%\n")

# ---------------------------------------------------------------
# 3. BANDS FOR NUMERIC COLUMNS
# ---------------------------------------------------------------
df["income_band"] = pd.qcut(
    df["MonthlyIncome"], 4,
    labels=["Q1 lowest income", "Q2", "Q3", "Q4 highest income"],
)
df["age_band"] = pd.cut(
    df["Age"], [17, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"],
)
df["tenure_band"] = pd.cut(
    df["YearsAtCompany"], [-1, 1, 3, 5, 10, 100],
    labels=["0-1 yrs", "2-3 yrs", "4-5 yrs", "6-10 yrs", "11+ yrs"],
)
df["promotion_band"] = pd.cut(
    df["YearsSinceLastPromotion"], [-1, 0, 2, 5, 100],
    labels=["0 yrs", "1-2 yrs", "3-5 yrs", "6+ yrs"],
)
df["overtime_income"] = df["OverTime"] + " / " + df["income_band"].astype(str)


def attrition_by(col):
    g = df.groupby(col, observed=True)["left"]
    t = pd.DataFrame({"employees": g.size(), "left": g.sum()})
    t["rate_pct"] = (t["left"] / t["employees"] * 100).round(1)
    t["vs_overall"] = (t["rate_pct"] / (overall * 100)).round(2)  # 1.0 = average
    t = t[t["employees"] >= MIN_GROUP].sort_values("rate_pct", ascending=False)
    return t


# ---------------------------------------------------------------
# 4. ATTRITION RATE BY EACH FACTOR
# ---------------------------------------------------------------
factors = [
    "OverTime", "JobRole", "Department", "Gender", "MaritalStatus",
    "BusinessTravel", "EducationField", "Education", "JobLevel",
    "StockOptionLevel", "WorkLifeBalance", "JobSatisfaction",
    "EnvironmentSatisfaction", "income_band", "age_band", "tenure_band",
    "promotion_band", "overtime_income",
]

spreads = []
for col in factors:
    table = attrition_by(col)
    print(f"ATTRITION BY {col.upper()}  (groups with at least {MIN_GROUP} employees)")
    print(table)
    print()
    table.to_csv(os.path.join(OUT_DIR, f"attrition_by_{col}.csv"))
    if len(table) > 1:
        spreads.append((col, table["rate_pct"].max(), table["rate_pct"].min()))

# ---------------------------------------------------------------
# 5. WHICH FACTORS SEPARATE STAYERS FROM LEAVERS THE MOST?
#    spread = highest group rate minus lowest group rate
# ---------------------------------------------------------------
summary = pd.DataFrame(spreads, columns=["factor", "highest_rate_pct", "lowest_rate_pct"])
summary["spread_pts"] = (summary["highest_rate_pct"] - summary["lowest_rate_pct"]).round(1)
summary = summary.sort_values("spread_pts", ascending=False)
print("FACTORS RANKED BY SPREAD (bigger spread = bigger difference between groups)")
print(summary.to_string(index=False))
summary.to_csv(os.path.join(OUT_DIR, "factor_ranking.csv"), index=False)

print("\nReminder: these are associations, not proof of cause. Compare each")
print("finding with what your Power BI dashboard shows before you publish it.")
