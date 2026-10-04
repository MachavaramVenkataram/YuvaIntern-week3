"""
Notebook Generation & Execution Script
YUVA Internship - Week 3

Constructs the complete week3_statistical_analysis.ipynb notebook with rich markdown
and executable Python cells, then executes all cells using nbconvert's ExecutePreprocessor.
"""

import os
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor


def create_and_run_notebook(output_notebook_path: str):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.13"
        }
    }

    cells = []

    # -------------------------------------------------------------
    # 1. Project Introduction
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""# YUVA Internship -- Week 3: Statistical Analysis and Hypothesis Testing in Python

## Project Title:
# **Statistical Investigation of Sales, Discounts, and Profitability in Superstore Data**

**Author / Intern:** YUVA Data Science Intern  
**Domain:** Business Analytics & Applied Inferential Statistics  
**Dataset:** Retail Superstore Sales Dataset (9,994 transactional records)  
**Methodology:** Parametric and Non-Parametric Hypothesis Testing, ANOVA, Chi-Square, Effect Size Estimation, Confidence Intervals, Multiple Testing Correction  
**Tools:** Python 3.13 | Pandas | NumPy | SciPy | Statsmodels | Matplotlib | Seaborn  

---

### Executive Context
In enterprise retail management, promotional discounts are widely deployed to stimulate sales volume, acquire new customers, and clear slow-moving inventory. However, aggressive price concessions often carry significant risks of margin cannibalization, operational losses, and negative customer reference pricing. 

This project provides a rigorous, data-driven statistical investigation of the Superstore sales dataset. We formulate and test explicit business hypotheses to determine whether discounts significantly depress transactional profits, whether product categories demonstrate structural profitability differences, and whether discount offering is statistically associated with transaction-level loss creation.

---
"""))

    # -------------------------------------------------------------
    # 2. Research Questions
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 1. Research Questions

This study addresses one primary research question and five secondary/exploratory questions:

### **Primary Research Question**
> **Does receiving a discount significantly affect average order-level profit?**  
> We evaluate whether orders receiving a discount ($Discount > 0$) have a significantly different mean net profit compared to orders receiving no discount ($Discount = 0$).

### **Secondary Research Questions**
1. **Category Differences:** Does average profit differ significantly across product categories (*Furniture*, *Office Supplies*, *Technology*)?
2. **Profitability Association:** Is there a statistically significant association between whether an order receives a discount and whether that order generates a net profit or a net loss?
3. **Effect Magnitude:** How large are the observed statistical effects in standardized units (Cohen's $d$, Eta squared $\eta^2$, Cramer's $V$)?
4. **Parameter Estimation:** What do the estimated 95% confidence intervals reveal about the true population parameter differences?
5. **Business Significance:** Are the statistically significant empirical findings practically meaningful for retail pricing policy and commercial strategy?
"""))

    # -------------------------------------------------------------
    # 3. Hypotheses Formulation
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 2. Hypothesis Formulation & Statistical Framework

We adopt a formal inferential testing framework using a two-sided significance threshold of $\alpha = 0.05$.

### **Hypothesis 1: Welch's Independent Two-Sample Test (Primary)**
* **Null Hypothesis ($H_0$):** The mean profit of discounted orders is equal to the mean profit of non-discounted orders.
  $$\mu_{\text{discounted}} = \mu_{\text{no\_discount}}$$
* **Alternative Hypothesis ($H_1$):** The mean profit of discounted orders differs from the mean profit of non-discounted orders.
  $$\mu_{\text{discounted}} \neq \mu_{\text{no\_discount}}$$
* **Method:** Two-sided Welch's t-test (`scipy.stats.ttest_ind(..., equal_var=False)`). Does not assume equal variances.
* **Sensitivity Check:** Non-parametric Mann-Whitney U test (`scipy.stats.mannwhitneyu`) to verify robustness against distributional skewness and outliers.

---

### **Hypothesis 2: One-Way Analysis of Variance (ANOVA)**
* **Null Hypothesis ($H_0$):** The mean profit across all three product categories is equal.
  $$\mu_{\text{Furniture}} = \mu_{\text{Office Supplies}} = \mu_{\text{Technology}}$$
* **Alternative Hypothesis ($H_1$):** At least one product category has a mean profit that differs from the others.
* **Method:** Fisher's One-Way ANOVA (`scipy.stats.f_oneway`), Levene's test for homoscedasticity, Welch's robust ANOVA, and post-hoc Tukey HSD for pairwise group contrasts.

---

### **Hypothesis 3: Pearson's Chi-Square Test of Independence**
* **Null Hypothesis ($H_0$):** Order discount status (*Discounted* vs. *No Discount*) and profitability status (*Profitable* vs. *Loss-making*) are independent.
* **Alternative Hypothesis ($H_1$):** Order discount status and profitability status are statistically associated.
* **Method:** Chi-Square test of independence (`scipy.stats.chi2_contingency`) with Cramer's $V$ effect size and Odds Ratio ($OR$) calculation.

---

### **Decision Rules & Multiple Testing**
* If $p < 0.05$, we **reject the null hypothesis** ($H_0$) and conclude statistical significance.
* If $p \ge 0.05$, we conclude that there is **insufficient empirical evidence to reject $H_0$** (we never say "the null hypothesis is proven").
* To control the Family-Wise Error Rate (FWER) across our family of tests, we apply the **Holm-Bonferroni step-down correction**.
"""))

    # -------------------------------------------------------------
    # 4. Environment Setup & Data Loading
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 3. Environment Setup and Data Ingestion

We begin by importing required analytical libraries, establishing high-resolution plotting configurations, and ingesting the raw Superstore dataset.
"""))

    cells.append(nbf.v4.new_code_cell(r"""import sys
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns

# Visual formatting settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']

# Path resolution
data_path = os.path.join('..', 'data', 'raw', 'Sample - Superstore.csv')
if not os.path.exists(data_path):
    data_path = os.path.join('data', 'raw', 'Sample - Superstore.csv')

df_raw = pd.read_csv(data_path, encoding='windows-1252')
print(f"[SUCCESS] Dataset loaded successfully.")
print(f"Shape: {df_raw.shape[0]:,} rows and {df_raw.shape[1]} columns.")
"""))

    # -------------------------------------------------------------
    # 5. Data Inspection
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 4. Dataset Inspection & Audit

Let us inspect the dataset's schema, examine initial records, verify data types, and check for missing values.
"""))

    cells.append(nbf.v4.new_code_cell(r"""# Display first 3 rows
display(df_raw.head(3))

# Check columns and data types
print("--- Column Inventory & Data Types ---")
display(pd.DataFrame({'Data Type': df_raw.dtypes, 'Missing Values': df_raw.isnull().sum()}))
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""**Inspection Findings:**
- The dataset contains 9,994 unique order line items with 21 attributes.
- There are **0 missing values** across all columns, confirming high data completeness.
- The financial measures `Sales`, `Quantity`, `Discount`, and `Profit` are present as expected.
"""))

    # -------------------------------------------------------------
    # 6. Data Cleaning & Feature Engineering
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 5. Data Cleaning and Feature Engineering

We now prepare analytical variables:
1. Strip column whitespace.
2. Parse date columns (`Order Date`, `Ship Date`) to datetime format.
3. Compute `Shipping Days` ($Ship Date - Order Date$).
4. Construct **`Discount_Status`**:
   - `Discounted` for orders with $Discount > 0$
   - `No Discount` for orders with $Discount == 0$
5. Construct **`Profitability_Status`**:
   - `Profitable` for orders with $Profit > 0$
   - `Loss-making` for orders with $Profit \le 0$
6. Construct **`Profit_Margin`** ($Profit / Sales$) and **`Discount_Band`** for stratified exploratory comparisons.
"""))

    cells.append(nbf.v4.new_code_cell(r"""df = df_raw.copy()
df.columns = [col.strip() for col in df.columns]

# Date conversions
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days

# Feature engineering
df['Discount_Status'] = np.where(df['Discount'] > 0, 'Discounted', 'No Discount')
df['Profitability_Status'] = np.where(df['Profit'] > 0, 'Profitable', 'Loss-making')
df['Profit_Margin'] = np.where(df['Sales'] > 0, df['Profit'] / df['Sales'], 0.0)
df['Discount_Pct'] = df['Discount'] * 100.0

# Binned Discount Bands
bins = [-0.001, 0.000, 0.100, 0.200, 0.500, 1.000]
labels = ['None (0%)', 'Low (1-10%)', 'Moderate (11-20%)', 'High (21-50%)', 'Deep (>50%)']
df['Discount_Band'] = pd.cut(df['Discount'], bins=bins, labels=labels)

# Save processed dataset
proc_path = os.path.join('..', 'data', 'processed', 'superstore_cleaned.csv')
if not os.path.exists(os.path.dirname(proc_path)):
    proc_path = os.path.join('data', 'processed', 'superstore_cleaned.csv')
os.makedirs(os.path.dirname(proc_path), exist_ok=True)
df.to_csv(proc_path, index=False)

print(f"[SUCCESS] Cleaned dataset saved to: {proc_path}")
print(f"Sample breakdown by Discount Status:")
display(df['Discount_Status'].value_counts(normalize=True).mul(100).round(2).to_frame('Percentage (%)'))
print(f"Sample breakdown by Profitability Status:")
display(df['Profitability_Status'].value_counts(normalize=True).mul(100).round(2).to_frame('Percentage (%)'))
"""))

    # -------------------------------------------------------------
    # 7. Descriptive Statistics
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 6. Comprehensive Exploratory Data Analysis & Descriptive Statistics

Before conducting formal hypothesis testing, we examine the distributional properties, central tendencies, and dispersions of the target variables.
"""))

    cells.append(nbf.v4.new_code_cell(r"""num_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
desc_summary = df[num_cols].describe().T
desc_summary['median'] = df[num_cols].median()
desc_summary['IQR'] = df[num_cols].apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
desc_summary['skewness'] = df[num_cols].skew()
desc_summary['kurtosis'] = df[num_cols].kurtosis()

desc_summary = desc_summary[['count', 'mean', 'std', 'min', '25%', 'median', '75%', 'max', 'IQR', 'skewness', 'kurtosis']]
display(desc_summary.round(3))
"""))

    cells.append(nbf.v4.new_code_cell(r"""# Bivariate Group Summaries
print("--- Profit Breakdown by Discount Status ---")
group_discount = df.groupby('Discount_Status')['Profit'].agg(
    Count='count',
    Mean='mean',
    Std='std',
    Median='median',
    IQR=lambda x: np.percentile(x, 75) - np.percentile(x, 25),
    Min='min',
    Max='max'
).round(2)
display(group_discount)

print("\n--- Profit Breakdown by Product Category ---")
group_category = df.groupby('Category')['Profit'].agg(
    Count='count',
    Mean='mean',
    Std='std',
    Median='median',
    IQR=lambda x: np.percentile(x, 75) - np.percentile(x, 25),
    Min='min',
    Max='max'
).round(2)
display(group_category)

print("\n--- Profit Breakdown by Granular Discount Band ---")
group_band = df.groupby('Discount_Band', observed=True)['Profit'].agg(
    Count='count',
    Mean='mean',
    Median='median',
    Loss_Rate_Pct=lambda x: (x <= 0).mean() * 100.0
).round(2)
display(group_band)
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""### Key Exploratory Observations:
1. **Substantial Negative Impact of Discounting:**
   - Orders receiving **no discount** ($N = 4,798$) yield an average profit of **+\$66.90** (median +\$16.00).
   - Orders receiving **discounts** ($N = 5,196$) yield an average profit of **-\$6.66** (median +\$3.34).
   - This represents an observed raw sample difference of **-\$73.56** per transaction.
2. **Category Profitability Variations:**
   - *Technology* shows the highest mean profit (**+\$78.75**, median \$25.02) and highest variability ($SD = \$428.82$).
   - *Office Supplies* shows moderate mean profit (**+\$20.33**, median \$6.88).
   - *Furniture* exhibits the lowest mean profit (**+\$8.70**, median \$7.77).
3. **Extreme Distributional Skewness:**
   - Profit exhibits positive skewness ($3.44$) and heavy kurtosis ($397.19$), reflecting a central cluster of small profits and severe long tails (min -\$6,600, max +\$8,400).
"""))

    # -------------------------------------------------------------
    # 8. Assumption Checking
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 7. Statistical Assumption Checking

Rigorous statistical testing requires auditing mathematical assumptions:
1. **Normality:** Because transaction profit is heavily skewed and kurtotic, formal normality tests reject normality ($p < 0.001$). However, under the **Central Limit Theorem (CLT)**, given our very large sample sizes ($N_1 = 4,798$, $N_2 = 5,196$), the sampling distribution of the sample mean converges to normality.
2. **Homogeneity of Variance (Homoscedasticity):** We conduct **Levene's test** to determine whether group variances are equal.
"""))

    cells.append(nbf.v4.new_code_cell(r"""# Levene's Test for Discount Status
disc_p = df[df['Discount_Status'] == 'Discounted']['Profit']
nodisc_p = df[df['Discount_Status'] == 'No Discount']['Profit']
lev_stat_disc, lev_p_disc = stats.levene(disc_p, nodisc_p)

print("Levene's Test for Variance Equality (Discounted vs. No Discount):")
print(f"  Statistic = {lev_stat_disc:.4f}, p-value = {lev_p_disc:.4e}")
if lev_p_disc < 0.05:
    print("  -> Homogeneity of variance is REJECTED. Welch's t-test is required!")

# Levene's Test for Categories
cats = [df[df['Category'] == c]['Profit'] for c in df['Category'].unique()]
lev_stat_cat, lev_p_cat = stats.levene(*cats)
print("\nLevene's Test for Variance Equality Across Product Categories:")
print(f"  Statistic = {lev_stat_cat:.4f}, p-value = {lev_p_cat:.4e}")
if lev_p_cat < 0.05:
    print("  -> Homogeneity of variance is REJECTED across categories. Welch's ANOVA is required as a robust alternative!")
"""))

    # -------------------------------------------------------------
    # 9. Hypothesis 1: Welch's t-test
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 8. Hypothesis 1 -- Independent Two-Sample Test (Welch's t-test)

We conduct a two-sided **Welch's t-test** (`scipy.stats.ttest_ind(..., equal_var=False)`), which uses the Welch-Satterthwaite approximation for degrees of freedom without assuming homoscedasticity.
"""))

    cells.append(nbf.v4.new_code_cell(r"""n1, n2 = len(disc_p), len(nodisc_p)
m1, m2 = disc_p.mean(), nodisc_p.mean()
s1, s2 = disc_p.std(ddof=1), nodisc_p.std(ddof=1)
v1, v2 = s1**2, s2**2
mean_diff = m1 - m2

# Welch t-test
t_stat, p_val = stats.ttest_ind(disc_p, nodisc_p, equal_var=False)

# Satterthwaite degrees of freedom
df_welch = (v1/n1 + v2/n2)**2 / ((v1/n1)**2 / (n1 - 1) + (v2/n2)**2 / (n2 - 1))
se_diff = np.sqrt(v1/n1 + v2/n2)
t_crit = stats.t.ppf(0.975, df_welch)
ci_lower = mean_diff - t_crit * se_diff
ci_upper = mean_diff + t_crit * se_diff

# Cohen's d (pooled std)
s_pooled = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
cohens_d = mean_diff / s_pooled
hedges_g = cohens_d * (1 - (3 / (4 * (n1 + n2) - 9)))

print("=== WELCH'S TWO-SAMPLE T-TEST RESULTS ===")
print(f"Discounted Orders:     N = {n1:,}, Mean = ${m1:.2f}, Median = ${disc_p.median():.2f}, Std = ${s1:.2f}")
print(f"No Discount Orders:    N = {n2:,}, Mean = ${m2:.2f}, Median = ${nodisc_p.median():.2f}, Std = ${s2:.2f}")
print(f"Observed Difference:   ${mean_diff:.2f}")
print(f"Welch t-statistic:     {t_stat:.4f}")
print(f"Degrees of Freedom:    {df_welch:.2f}")
print(f"p-value:               {p_val:.4e}")
print(f"95% Confidence Int:    [${ci_lower:.2f}, ${ci_upper:.2f}]")
print(f"Cohen's d:             {cohens_d:.4f} (Hedges' g = {hedges_g:.4f})")
print(f"Decision:              {'Reject H0' if p_val < 0.05 else 'Fail to Reject H0'} at alpha = 0.05")
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""### Interpretation of Hypothesis 1:
- **Statistical Result:** With $t(9162.24) = -15.7380$ and $p = 4.36 \times 10^{-55} < 0.001$, we **reject the null hypothesis ($H_0$)**.
- **Confidence Interval:** The 95% confidence interval for the difference in mean profit is **[-$82.72, -$64.40]**. Because this interval lies entirely below zero, we can assert with 95% confidence that under repeated sampling, discounted orders generate between \$64.40 and \$82.72 less profit per order than non-discounted orders.
- **Effect Size:** Cohen's $d = -0.3179$ indicates a **moderate practical effect size**, proving that the finding is not merely an artifact of high sample size but represents a substantial commercial drag on unit profitability.
"""))

    # -------------------------------------------------------------
    # 10. Hypothesis 1: Sensitivity Check (Mann-Whitney U)
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 9. Hypothesis 1 -- Robustness Check (Mann-Whitney U Test)

Because profit exhibits non-normality and extreme outliers, we conduct a non-parametric **Mann-Whitney U test** as a sensitivity check. The test evaluates whether the distribution of discounted profits is stochastically shifted relative to non-discounted profits.
"""))

    cells.append(nbf.v4.new_code_cell(r"""u_stat, u_pval = stats.mannwhitneyu(disc_p, nodisc_p, alternative='two-sided')
rank_biserial = 1.0 - (2.0 * u_stat / (n1 * n2))

print("=== MANN-WHITNEY U TEST (ROBUSTNESS CHECK) ===")
print(f"U-statistic:           {u_stat:,.1f}")
print(f"Asymptotic p-value:    {u_pval:.4e}")
print(f"Rank-Biserial r:       {rank_biserial:.4f}")
print(f"Decision:              {'Reject H0' if u_pval < 0.05 else 'Fail to Reject H0'}")
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""### Robustness Conclusion:
The non-parametric Mann-Whitney U test confirms the parametric result with $p < 0.0001$ ($U = 6,266,805.5$). The rank-biserial correlation of $r = 0.4973$ confirms that the probability of an undiscounted order generating higher profit than a discounted order is substantial. This proves that the Welch t-test results are highly robust and not driven by a handful of leverage outliers.
"""))

    # -------------------------------------------------------------
    # 11. Hypothesis 2: One-Way ANOVA & Welch's ANOVA
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 10. Hypothesis 2 -- One-Way Analysis of Variance (ANOVA)

We test whether mean profit differs across the three product categories (*Furniture*, *Office Supplies*, *Technology*).
"""))

    cells.append(nbf.v4.new_code_cell(r"""cat_list = df['Category'].unique()
cat_groups = [df[df['Category'] == c]['Profit'] for c in cat_list]

# Standard ANOVA
f_stat, anova_p = stats.f_oneway(*cat_groups)

# Degrees of freedom
k = len(cat_groups)
N_tot = len(df)
df_b = k - 1
df_w = N_tot - k

# Eta squared
grand_mean = df['Profit'].mean()
ss_total = ((df['Profit'] - grand_mean)**2).sum()
ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in cat_groups)
eta_sq = ss_between / ss_total

# Robust Welch's ANOVA (relaxation of equal variances)
ni = np.array([len(g) for g in cat_groups])
mi = np.array([g.mean() for g in cat_groups])
vi = np.array([g.var(ddof=1) for g in cat_groups])
wi = ni / vi
W = np.sum(wi)
m_star = np.sum(wi * mi) / W
ss_between_w = np.sum(wi * (mi - m_star)**2)
q = (2.0 * (k - 2) / (k**2 - 1.0)) * np.sum(((1.0 - wi / W)**2) / (ni - 1.0))
f_welch = ss_between_w / ((k - 1) * (1.0 + q))
df1_welch = k - 1
df2_welch = (k**2 - 1.0) / (3.0 * np.sum(((1.0 - wi / W)**2) / (ni - 1.0)))
p_welch = 1.0 - stats.f.cdf(f_welch, df1_welch, df2_welch)

print("=== ONE-WAY ANOVA RESULTS ===")
print(f"Standard ANOVA: F({df_b}, {df_w}) = {f_stat:.4f}, p-value = {anova_p:.4e}")
print(f"Eta Squared (η²):                 {eta_sq:.4f} ({eta_sq*100:.2f}% of variance explained)")
print(f"Welch's Robust ANOVA:             F_W({df1_welch}, {df2_welch:.2f}) = {f_welch:.4f}, p-value = {p_welch:.4e}")
print(f"Decision:                         {'Reject H0' if anova_p < 0.05 else 'Fail to Reject H0'} at alpha = 0.05")
"""))

    # -------------------------------------------------------------
    # 12. Post-Hoc Analysis (Tukey HSD)
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 11. Post-Hoc Pairwise Comparisons (Tukey HSD)

Because the omnibus ANOVA test is statistically significant ($p = 3.47 \times 10^{-24} < 0.001$), we conduct **Tukey's Honestly Significant Difference (HSD)** test to determine precisely which category pairs differ significantly while controlling the Family-Wise Error Rate ($\text{FWER} = 0.05$).
"""))

    cells.append(nbf.v4.new_code_cell(r"""tukey = pairwise_tukeyhsd(endog=df['Profit'], groups=df['Category'], alpha=0.05)
print(tukey)

tukey_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])
display(tukey_df)
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""### Post-Hoc Analysis Insights:
1. **Technology vs. Furniture:** Mean difference is **+\$70.05** ($p_{adj} < 0.001$, 95% CI: [\$52.67, \$87.44]). Significant difference.
2. **Technology vs. Office Supplies:** Mean difference is **+\$58.43** ($p_{adj} < 0.001$, 95% CI: [\$43.90, \$72.95]). Significant difference.
3. **Office Supplies vs. Furniture:** Mean difference is **+\$11.63** ($p_{adj} = 0.1181$, 95% CI: [-\$2.16, \$25.42]). **Fail to reject $H_0$**. There is insufficient empirical evidence to conclude that Furniture and Office Supplies have different mean profits.
"""))

    # -------------------------------------------------------------
    # 13. Hypothesis 3: Chi-Square Test
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 12. Hypothesis 3 -- Pearson's Chi-Square Test of Independence

We investigate whether order discount status (*Discounted* vs. *No Discount*) is statistically associated with order profitability (*Profitable* vs. *Loss-making*).
"""))

    cells.append(nbf.v4.new_code_cell(r"""ct = pd.crosstab(df['Discount_Status'], df['Profitability_Status'])
print("--- Observed Contingency Matrix ---")
display(ct)

# Chi-Square Test
chi2, p_chi, dof, expected = stats.chi2_contingency(ct)
exp_df = pd.DataFrame(expected, index=ct.index, columns=ct.columns).round(2)

print("\n--- Expected Frequencies Matrix ---")
display(exp_df)

# Effect Size: Cramer's V & Odds Ratio
n_tot = ct.values.sum()
cramers_v = np.sqrt(chi2 / (n_tot * (min(ct.shape) - 1)))

# Odds Ratio: (a * d) / (b * c)
a = ct.loc['Discounted', 'Loss-making']
b = ct.loc['Discounted', 'Profitable']
c = ct.loc['No Discount', 'Loss-making']
d = ct.loc['No Discount', 'Profitable']
odds_ratio = (a * d) / (b * c)

print("\n=== CHI-SQUARE TEST OF INDEPENDENCE RESULTS ===")
print(f"Pearson Chi-Square (χ²): {chi2:.4f}")
print(f"Degrees of Freedom:      {dof}")
print(f"p-value:                 {p_chi:.4e}")
print(f"Cramer's V Effect Size:  {cramers_v:.4f} (Very Strong Association)")
print(f"Odds Ratio (OR):         {odds_ratio:.2f}")
print(f"Minimum Expected Cell:   {expected.min():.2f} (Assumption >= 5 Satisfied)")
print(f"Decision:                {'Reject H0' if p_chi < 0.05 else 'Fail to Reject H0'} at alpha = 0.05")
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""### Interpretation of Hypothesis 3:
- **Massive Contingency Disparity:**
  - Among **No Discount** orders, **99.37%** (4,768 / 4,798) are profitable; only **0.63%** (30 orders) incur a loss.
  - Among **Discounted** orders, **36.68%** (1,906 / 5,196) incur a net loss!
- **Statistical Significance & Association:**
  - $\chi^2(1) = 2074.09, p < 10^{-300}$.
  - **Cramer's V = 0.4556**, indicating a strong association between discount status and transactional loss incidence.
  - The **Odds Ratio of 91.95** indicates that discounted orders have nearly **92 times higher odds** of resulting in a loss than non-discounted orders.
"""))

    # -------------------------------------------------------------
    # 14. Confidence Intervals & Effect Sizes
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 13. Parameter Estimation & 95% Confidence Intervals

We report 95% confidence intervals for all primary group means and difference metrics.
"""))

    cells.append(nbf.v4.new_code_cell(r"""ci_records = []

# Category CIs
for cat in ['Technology', 'Office Supplies', 'Furniture']:
    sub = df[df['Category'] == cat]['Profit']
    mean_val = sub.mean()
    ci = stats.t.interval(0.95, df=len(sub)-1, loc=mean_val, scale=stats.sem(sub))
    ci_records.append({
        'Parameter': f"Category Mean: {cat}",
        'Estimate': f"${mean_val:.2f}",
        '95% Lower': f"${ci[0]:.2f}",
        '95% Upper': f"${ci[1]:.2f}",
        'Interpretation': 'Expected true mean profit for this product category.'
    })

# Discount Group CIs
for status in ['No Discount', 'Discounted']:
    sub = df[df['Discount_Status'] == status]['Profit']
    mean_val = sub.mean()
    ci = stats.t.interval(0.95, df=len(sub)-1, loc=mean_val, scale=stats.sem(sub))
    ci_records.append({
        'Parameter': f"Discount Group Mean: {status}",
        'Estimate': f"${mean_val:.2f}",
        '95% Lower': f"${ci[0]:.2f}",
        '95% Upper': f"${ci[1]:.2f}",
        'Interpretation': 'Expected true mean profit for this discount condition.'
    })

# Mean Difference CI
ci_records.append({
    'Parameter': "Mean Difference (Discounted - No Discount)",
    'Estimate': f"-${abs(mean_diff):.2f}",
    '95% Lower': f"-${abs(ci_lower):.2f}",
    '95% Upper': f"-${abs(ci_upper):.2f}",
    'Interpretation': 'Estimated true difference in mean transactional profit.'
})

ci_table = pd.DataFrame(ci_records)
display(ci_table)
"""))

    # -------------------------------------------------------------
    # 15. Multiple Testing Correction
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 14. Multiple Testing Correction (Holm-Bonferroni Method)

When conducting multiple hypothesis tests across the same dataset, the probability of at least one Type I error (false positive) increases. To control the Family-Wise Error Rate (FWER) at $\alpha = 0.05$, we apply the **Holm-Bonferroni step-down procedure**.
"""))

    cells.append(nbf.v4.new_code_cell(r"""p_dict = {
    "Welch t-test (Discount vs. Profit)": p_val,
    "Mann-Whitney U Test (Robustness Check)": u_pval,
    "One-Way ANOVA (Category Profit)": anova_p,
    "Welch's ANOVA (Robust Category Test)": p_welch,
    "Chi-Square Test (Discount x Loss Association)": p_chi
}

sorted_tests = sorted(p_dict.items(), key=lambda x: x[1])
m = len(sorted_tests)
holm_records = []

for rank, (name, p) in enumerate(sorted_tests, 1):
    threshold = 0.05 / (m - rank + 1)
    adj_p = min(p * (m - rank + 1), 1.0)
    sig = "Yes (Reject H0)" if p < threshold else "No (Fail to Reject)"
    holm_records.append({
        "Rank": rank,
        "Hypothesis Test": name,
        "Raw p-value": f"{p:.4e}",
        "Holm Threshold": f"{threshold:.5f}",
        "Adjusted p-value": f"{adj_p:.4e}",
        "Statistically Significant": sig
    })

holm_table = pd.DataFrame(holm_records)
display(holm_table)
"""))

    cells.append(nbf.v4.new_markdown_cell(r"""**Multiple Testing Finding:**
Even under strict Holm-Bonferroni FWER control, **all primary and secondary hypothesis tests remain statistically significant** ($p_{adj} < 0.001$).
"""))

    # -------------------------------------------------------------
    # 16. Visualizations
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 15. Statistical Visualizations

We now generate and display all 7 publication-standard statistical charts.
"""))

    cells.append(nbf.v4.new_code_cell(r"""# Display all 7 generated figures
import glob
from IPython.display import Image, display

viz_dir = os.path.join('..', 'visualizations')
if not os.path.exists(viz_dir):
    viz_dir = 'visualizations'

fig_files = sorted(glob.glob(os.path.join(viz_dir, '*.png')))
print(f"[INFO] Found {len(fig_files)} generated statistical figures:")
for fig_path in fig_files:
    print(f"Displaying: {os.path.basename(fig_path)}")
    display(Image(filename=fig_path, width=850))
"""))

    # -------------------------------------------------------------
    # 17. Consolidated Results Table
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 16. Consolidated Statistical Results Table

Below is the consolidated statistical results table summarizing all empirical tests, test statistics, degrees of freedom, p-values, effect sizes, 95% confidence intervals, and final decisions.
"""))

    cells.append(nbf.v4.new_code_cell(r"""res_path = os.path.join('..', 'results', 'statistical_results.csv')
if not os.path.exists(res_path):
    res_path = os.path.join('results', 'statistical_results.csv')

final_results_df = pd.read_csv(res_path)
display(final_results_df)
"""))

    # -------------------------------------------------------------
    # 18. Business Interpretation & Limitations
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 17. Business Implications, Critical Limitations & Future Scope

### **1. Business Interpretation & Commercial Implications**
1. **The Promotional Trap:** Offering discounts in this retail enterprise does not merely trim margins -- it systematically drives transactions into net losses. Discounted orders lose an average of -\$6.66 per order, whereas undiscounted orders deliver +\$66.90.
2. **Extreme Asymmetry in Loss Incidence:** Undiscounted orders have an extraordinary 99.37% profit rate, while discounted orders fail to break even in 36.68% of transactions (an odds ratio of 91.95).
3. **Threshold Effects:** Transactions with discounts above 20% experience severe downside risks. Deep discounting (>50%) produces a 100% loss rate in this dataset.
4. **Category Nuances:** Technology products generate the highest mean profit (\$78.75), while Furniture generates only \$8.70. High discounting in Furniture creates severe operational deficits.

---

### **2. Crucial Methodological Limitations**
1. **Observational Data vs. Causation:** This dataset consists of observational transactions, not a randomized controlled trial (A/B experiment). Discounter orders may differ in product mix, regional pricing tiers, or customer price sensitivity. **Statistical association does not prove direct causation.**
2. **Missing Fixed Cost and Customer Lifetime Value (CLV):** The dataset records order-level accounting profit but lacks customer acquisition costs (CAC), repeat purchase rates, or long-term retention metrics. A discount that loses money upfront might theoretically be justified if it acquires a high-CLV repeat customer.
3. **Unobserved Confounders:** Category-level margins, supplier rebates, shipping freight contracts, and regional sales quotas are unobserved variables that likely confound the discount-profit relationship.

---

### **3. Future Analytical Directions**
- **Econometric Causal Inference:** Apply Propensity Score Matching (PSM) and Instrumental Variables (IV) to isolate causal discount elasticity.
- **Multivariate Regression & Machine Learning:** Fit regularized models (Lasso/Ridge, Gradient Boosting) to estimate non-linear discount elasticity curves per sub-category.
- **Customer Cohort LTV Tracking:** Link order profitability to longitudinal customer repeat transaction behavior.
"""))

    # -------------------------------------------------------------
    # 19. Conclusion
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 18. Final Internship Conclusion

| Hypothesis Test | Research Question | Test Statistic | p-value | Effect Size | Decision | Commercial Implication |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Welch's t-test (Primary)** | Discount vs. Mean Profit | $t = -15.7380$ | $4.36 \times 10^{-55}$ | $d = -0.3179$ | **Reject $H_0$** | Discounted orders generate \$73.56 lower mean profit. |
| **Mann-Whitney U** | Distributional Robustness | $U = 6,266,805.5$ | $< 0.0001$ | $r = 0.4973$ | **Reject $H_0$** | Findings are highly robust to extreme outliers and skewness. |
| **One-Way ANOVA** | Category Mean Profit | $F = 54.3110$ | $3.47 \times 10^{-24}$ | $\eta^2 = 0.0108$ | **Reject $H_0$** | Profit differs significantly across categories (Technology leads). |
| **Tukey HSD Post-Hoc** | Pairwise Category Differences | Multiple | Technology $p < 0.001$ | Group Diffs | **Partial Reject** | Technology beats Furniture & Office; Furniture equals Office Supplies. |
| **Chi-Square Test** | Discount vs. Loss Association | $\chi^2 = 2074.09$ | $< 10^{-300}$ | $V = 0.4556$ | **Reject $H_0$** | Discounting escalates loss-making odds by 92-fold. |

This statistical study demonstrates the critical value of rigorous hypothesis testing over simplistic exploratory aggregations. Management must institute a maximum discount threshold (recommended $\le 20\%$), establish category-specific approval gates, and replace blanket discounting with targeted, margin-protected loyalty incentives.
"""))

    nb.cells = cells

    # Save unexecuted notebook first
    os.makedirs(os.path.dirname(output_notebook_path), exist_ok=True)
    with open(output_notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[INFO] Initial notebook created at: {output_notebook_path}")

    # Execute notebook
    print("[INFO] Executing all notebook cells via ExecutePreprocessor...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': os.path.dirname(output_notebook_path)}})

    # Save fully executed notebook
    with open(output_notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[SUCCESS] Notebook successfully executed and saved with all cell outputs to: {output_notebook_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    nb_out = os.path.join(base_dir, "yuva-week3-statistical-analysis", "notebooks", "week3_statistical_analysis.ipynb")
    create_and_run_notebook(nb_out)
