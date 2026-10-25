# HR Analytics System – Employee Retention & Attrition 📊

I wanted to find out which groups of employees are most likely to leave a company, and where an HR team should look first. I explored the data in Python, calculated attrition rates by group with a script, and built a Power BI dashboard with filters for department, gender, and age.
# IBM HR Attrition Analysis (Power BI and Python)

I wanted to find out which groups of employees are most likely to leave a company, and where an HR team should look first. I explored the data in Python, calculated attrition rates by group with a script, and built a Power BI dashboard with filters for department, gender, and age.

![Dashboard overview](visuals/.png)

**Tools:** Power BI, Python (pandas, matplotlib, seaborn)
**Data:** 1,470 employees, 35 columns

## The question I was trying to answer

Which employee groups have the highest attrition, and where should HR focus first?

Throughout this project, **attrition rate** means the employees who left divided by all employees in that group. I use rates, not raw counts, because a big group will always have more leavers than a small one.

## The data

I used the IBM HR Analytics Employee Attrition dataset from Kaggle ([add the dataset link here]). Each row is one employee, with details like age, department, job role, monthly income, years at the company, overtime, and whether they left.

This is a **fictional dataset** created by IBM data scientists, so the patterns show how to analyze attrition, not what happens at a real company.

## What I did

1. Checked the data quality (missing values, duplicates, columns with no information).
2. Explored the data in Python (`EDA SCRIPT.ipynb`).
3. Calculated attrition rates for each factor with a script (`hr_analysis.py`), so every number below can be traced.
4. Built the Power BI dashboard (`IBM HR-Analytics Dashboard.pbix`) with KPI cards, charts, and slicers for department, gender, and age, plus an insights page and a recommendations page.
5. Checked the numbers on the dashboard against the script.

## Data checks

| Check | Result |
|---|---|
| Rows and columns | 1,470 rows, 35 columns |
| Missing values | None |
| Duplicate rows | None |
| Columns with a single value (no information) | EmployeeCount, Over18, StandardHours |
| Employee ID | EmployeeNumber is unique for every row |

The dataset is very clean, which is typical of a fictional dataset. Real HR data would need far more cleaning.

## What I found

**Overall, 237 of 1,470 employees left, an attrition rate of 16.1%.** Because only about 1 in 6 left, the "left" group is much smaller than the "stayed" group, so small groups can swing the rates.

**1. Overtime is the clearest single signal.**
Employees who work overtime left at 30.5% (127 of 416), compared with 10.4% (110 of 1,054) for those who don't, almost three times the rate.

**2. Low pay and overtime together are the highest-risk group.**
I split employees into four equal income groups. The lowest group earns under about 2,911 a month (the dataset doesn't state a currency). Among them, those who work overtime left at 58.5% (62 of 106). Employees who don't work overtime and are in the top half of income left at about 7%.

**3. Some job roles lose people much faster than others.**
Sales Representatives left at 39.8% (33 of 83), Laboratory Technicians at 23.9%, and Human Resources staff at 23.1%. At the other end, Research Directors left at 2.5% and Managers at 4.9%. Sales Representative is a small group, so treat that figure with some care.

**4. New and young employees leave most.**
Employees with 0 to 1 years at the company left at 34.9% (75 of 215), against 8.1% for those with 11 or more years. By age, the 18 to 25 group left at 35.8% (44 of 123), against 9.2% for ages 36 to 45. Leavers were younger on average: 33.6 years, versus 37.6 for those who stayed.

**5. The department with the most leavers is not the department with the highest rate.**
Research and Development had the most leavers (133 of 237, or 56%), but only because it is 65% of all employees. Its attrition rate is 13.8%, the lowest of the three departments. Sales (20.6%) and Human Resources (19.0%) have higher rates. This is why I compare rates and not counts.

**6. Other patterns worth noting.**
Single employees left at 25.5%, against 12.5% for married and 10.1% for divorced employees. Employees who travel frequently left at 24.9%, against 8.0% for those who don't travel. Employees with no stock options left at 24.4%, against 9.4% and 7.6% for option levels 1 and 2. Employees rating their work-life balance the lowest left at 31.2%, though that group is only 80 people.

**7. Gender is not a major driver here.**
Men left at 17.0% and women at 14.8%, a gap of 2.2 percentage points, much smaller than the gaps for overtime, tenure, or role.

**8. Pay matters.**
Leavers had a median monthly income of 3,202, against 5,204 for those who stayed. About 69% of leavers (163 of 237) earned under 5,000 a month, though that band is also about half of all employees (749 of 1,470), so the better comparison is the rate: 21.8% below 5,000 versus 11.1% for 5,000 to 10,000.

## What I would recommend

These recommendations follow from the numbers above:

1. **Review overtime workload and pay together, starting with lower-paid employees.** That group has the highest attrition (58.5% for the lowest income group working overtime).
2. **Strengthen onboarding and early-career support.** More than a third of employees in their first year or two leave, so improving the first year is likely the cheapest place to retain people.
3. **Look at Sales roles first, not R&D.** Sales Representatives and the Sales department have the highest rates, even though R&D has more leavers by count.
4. **Don't prioritize gender-based programs for attrition.** The gap is small in this data.

## Limits of this analysis

- **Association, not cause.** The data shows which groups leave more, not why. Reducing overtime might help, or the same underlying issue might drive both.
- **Fictional data.** Real patterns may differ.
- **Imbalanced data.** Only 16.1% of employees left, so some group rates rest on small numbers. I ignored groups smaller than 30 employees.
- **Snapshot.** There are no dates, so I can't see how attrition changes over time.
- **No predictive model.** This project describes who left. It does not predict who will leave.

## What's in this repo

| File | What it is |
|---|---|
| `IBM HR-Analytics Dashboard.pbix` | The Power BI dashboard |
| `EDA SCRIPT.ipynb` | Exploratory analysis in Python |
| `hr_analysis.py` | Script that calculates the attrition rates above |
| `WA_Fn-UseC_-HR-Employee-Attrition.csv` | The source data |
| `visuals/` | Dashboard screenshots |
| `outputs/` | Tables created by `hr_analysis.py` |

## Running it yourself

1. Put `hr_analysis.py` in the same folder as the CSV file.
2. Install pandas with `pip install pandas`, then run `python hr_analysis.py`. It prints the tables and saves them in an `outputs` folder.
3. Open `IBM HR-Analytics Dashboard.pbix` in Power BI Desktop. If it asks for the data source, point it to the CSV file.

Created by Sai Hemanth Botcha
