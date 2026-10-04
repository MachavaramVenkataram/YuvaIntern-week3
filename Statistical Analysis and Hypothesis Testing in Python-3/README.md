# YUVA Internship – Week 3: Statistical Analysis and Hypothesis Testing

## Statistical Investigation of Sales, Discounts, and Profitability in Superstore Data

**Author:** YUVA Data Science Intern  
**Program:** YUVA Internship Program  
**Track:** Data Science & Applied Statistical Modeling  
**Technology Stack:** Python 3.13 | Pandas | NumPy | SciPy | Statsmodels | Matplotlib | Seaborn | python-docx  

---

## Project Overview

In commercial retail management, promotional discounting is frequently deployed under the premise that lower prices stimulate sales volume sufficiently to maximize total gross margin. However, without rigorous statistical testing, pricing concessions can easily erode margins, create adverse customer selection, and result in severe transactional losses.

This project delivers a statistically rigorous, reproducible investigation of **9,994 order-level transactions** from the Superstore retail sales dataset. Rather than relying on simple aggregations or visualizations, we formulate and execute explicit hypothesis tests to evaluate:
1. Whether promotional discounting statistically depresses transactional profitability.
2. Whether product categories (*Furniture*, *Office Supplies*, *Technology*) demonstrate structural differences in mean profit.
3. Whether offering a discount is statistically associated with generating an operational financial loss.
4. The exact parameter boundaries estimated via 95% confidence intervals.
5. Standardized effect sizes (Cohen's $d$, Eta squared $\eta^2$, Cramer's $V$, and Odds Ratios) to gauge commercial relevance.

---

## Research Questions

### **Primary Research Question**
* **Does receiving a discount significantly affect average order-level profit?**  
  Specifically, do orders receiving a discount ($Discount > 0$) have a significantly different mean net profit compared to orders sold at list price ($Discount = 0$)?

### **Secondary Research Questions**
1. **Category Differences:** Does average profit differ significantly across merchandise categories (*Furniture*, *Office Supplies*, *Technology*)?
2. **Loss Association:** Is there a statistically significant association between order discount status and whether an order yields a net profit or an operational loss?
3. **Effect Magnitude:** How large are the observed statistical differences when standardized ($d$, $\eta^2$, $V$)?
4. **Parameter Estimation:** What do the estimated 95% confidence intervals reveal about the plausible true population values?
5. **Business Significance:** Are the statistically significant findings also meaningful from an operational and financial management perspective?

---

## Hypotheses

All tests are conducted at an a priori significance threshold of **$\alpha = 0.05$**.

### **Hypothesis 1: Welch's Independent Two-Sample Test (Primary)**
* **Null Hypothesis ($H_0$):** The mean profit of discounted orders is equal to the mean profit of non-discounted orders:
  $$\mu_{\text{discounted}} = \mu_{\text{no\_discount}}$$
* **Alternative Hypothesis ($H_1$):** The mean profit of discounted orders differs from the mean profit of non-discounted orders:
  $$\mu_{\text{discounted}} \neq \mu_{\text{no\_discount}}$$
* **Method:** Two-sided Welch's t-test (`scipy.stats.ttest_ind(..., equal_var=False)`), with non-parametric Mann-Whitney U test as a sensitivity/robustness check.

### **Hypothesis 2: One-Way Analysis of Variance (ANOVA)**
* **Null Hypothesis ($H_0$):** The population mean profit across all three merchandise categories is equal:
  $$\mu_{\text{Furniture}} = \mu_{\text{Office Supplies}} = \mu_{\text{Technology}}$$
* **Alternative Hypothesis ($H_1$):** At least one merchandise category has a mean profit that differs from the others.
* **Method:** One-Way ANOVA (`scipy.stats.f_oneway`), Levene's test for homoscedasticity, Welch's robust ANOVA, and post-hoc Tukey HSD pairwise contrasts.

### **Hypothesis 3: Pearson's Chi-Square Test of Independence**
* **Null Hypothesis ($H_0$):** Order discount status (*Discounted* vs. *No Discount*) and profitability status (*Profitable* vs. *Loss-making*) are independent.
* **Alternative Hypothesis ($H_1$):** Order discount status and profitability status are statistically associated.
* **Method:** Pearson's $\chi^2$ contingency test (`scipy.stats.chi2_contingency`) with Cramer's $V$ and Odds Ratio ($OR$).

---

## Dataset

* **Source:** Retail Superstore Sales Dataset (standard public enterprise retail benchmark).
* **Sample Size:** 9,994 transactional records across 21 variables.
* **Data Hygiene:** 0 missing values detected across all financial and categorical fields.
* **Key Variables:**
  - `Sales`: Gross transaction revenue ($0.44 to $22,638.48, mean $229.86).
  - `Quantity`: Units per order line (1 to 14, mean 3.79).
  - `Discount`: Rate applied (0.00 to 0.80, mean 0.156).
  - `Profit`: Accounting net profit (-$6,599.98 to +$8,399.98, mean $28.66, median $8.67).
  - `Category`: *Furniture* (2,121), *Office Supplies* (6,026), *Technology* (1,847).
  - `Discount_Status`: *Discounted* (5,196; 51.99%) vs. *No Discount* (4,798; 48.01%).
  - `Profitability_Status`: *Profitable* (8,058; 80.63%) vs. *Loss-making* (1,936; 19.37%).

---

## Statistical Methods

1. **Welch's Two-Sample t-Test:** Utilizes Satterthwaite degrees of freedom ($df = 9,162.24$) without assuming equal group variances (homoscedasticity was rejected by Levene's test, $p = 0.00033$).
2. **Mann-Whitney U Test:** Non-parametric rank-based robustness check confirming that results are not an artifact of extreme tail outliers or skewness ($p < 0.0001$).
3. **One-Way ANOVA & Welch's Robust ANOVA:** F-testing across product categories, complemented by Welch's ANOVA under variance inequality ($p < 0.0001$).
4. **Tukey HSD Post-Hoc Contrasts:** Controls Family-Wise Error Rate (FWER) across all pairwise category comparisons.
5. **Pearson's $\chi^2$ Test of Independence:** Cross-tabulation of a 2x2 contingency matrix (all expected cell frequencies $> 929$, far exceeding Cochran's rule of 5).
6. **Confidence Intervals:** 95% intervals computed via Student's $t$ distribution.
7. **Multiple Testing Correction:** Holm-Bonferroni step-down procedure applied to safeguard against false discoveries across the test family.

---

## Visualizations

All 7 publication-standard visualizations are generated at **300 DPI** and saved in `visualizations/`:

| File | Figure Title | Statistical Focus |
| :--- | :--- | :--- |
| `01_profit_distribution.png` | **Profit Distribution & Skewness** | Dual-panel log histogram + focused central KDE showing high skewness (+3.44) and kurtosis (+397.19). |
| `02_discount_vs_profit.png` | **Discount vs. Profit Scatter Plot** | Jittered scatter plot with OLS trend line demonstrating the severe loss cliff at discounts $> 20\%$. |
| `03_group_comparison.png` | **Discounted vs. No Discount Profit** | Truncated box plot and violin density profiles with diamond mean markers (-$6.66 vs +$66.90). |
| `04_category_profit_distribution.png` | **Category Profit Distributions** | Comparative box plots illustrating Technology's higher median and spread versus Furniture and Office Supplies. |
| `05_anova_comparison.png` | **ANOVA Category Means & 95% CIs** | Bar chart with 95% error whiskers, sample sizes, and Tukey HSD significance brackets. |
| `06_contingency_heatmap.png` | **Contingency Matrix Heatmap** | Dual heatmaps of absolute transaction counts and within-group row percentages (36.68% loss vs 0.63% loss). |
| `07_confidence_intervals.png` | **Confidence Intervals Summary** | Standardized forest plot showing 95% CIs for category means, discount groups, and the difference in means. |

---

## Consolidated Statistical Results

| Statistical Test | Research Question | Test Statistic & df | p-value | Standardized Effect Size | 95% Confidence Interval | Decision ($\alpha = 0.05$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Welch's t-test (Primary)** | Discount vs. Mean Profit | $t = -15.7380$, $df = 9162.24$ | $4.3569 \times 10^{-55}$ | Cohen's $d = -0.3179$ | [-$82.72, -$64.40] USD | **Reject $H_0$** |
| **Mann-Whitney U** | Rank Distribution Robustness | $U = 6,266,805.5$, Rank Sum | $< 0.0001$ | Rank-biserial $r = 0.4973$ | N/A | **Reject $H_0$** |
| **One-Way ANOVA** | Category Mean Differences | $F = 54.3110$, $df = (2, 9991)$ | $3.4699 \times 10^{-24}$ | $\eta^2 = 0.0108$ | Category specific | **Reject $H_0$** |
| **Welch's ANOVA** | Robust Category Test | $F_W = 24.0825$, $df = (2, 3587)$ | $4.0802 \times 10^{-11}$ | $\eta^2 = 0.0108$ | Category specific | **Reject $H_0$** |
| **Pearson's $\chi^2$ Test** | Discount x Profitability Status | $\chi^2 = 2074.0898$, $df = 1$ | $< 10^{-300}$ | Cramer's $V = 0.4556$ | Odds Ratio = 91.95 | **Reject $H_0$** |

### **Holm-Bonferroni FWER Control**
All raw $p$-values are orders of magnitude below their respective sequential thresholds (all $p_{\text{adj}} < 0.001$), confirming that all empirical discoveries remain decisive under strict multiple-testing control.

---

## Business Implications

1. **Abolish Blanket Discretionary Discounting:** Undiscounted orders deliver an average profit of **+$66.90**, while discounted orders generate an average loss of **-$6.66** (a net drag of -$73.56 per order). Discounting is not a margin trimmer; it is an active loss generator.
2. **The 20% Hard Ceiling:** Stratified analysis reveals that discounts $\le 20\%$ maintain positive average profitability, whereas discounts $> 20\%$ precipitate an **88.7% loss rate**, rising to **100.0%** for discounts $> 50\%$. Management must enforce an automated system block on unapproved discounts $> 20\%$.
3. **Protect Fragile Furniture Margins:** Furniture suffers from structural margin weakness (mean profit $8.70, loss rate 33.66%). Discretionary discounting in Furniture should be eliminated until supplier costs are renegotiated.
4. **Align Sales Compensation with Margin:** Sales commissions based on gross revenue incentivize aggressive price concessions. Compensation must be indexed to gross margin contribution to align sales behavior with enterprise profitability.

---

## Methodological Limitations

1. **Observational Data (Association vs. Causation):** The dataset records historical observational transactions rather than a randomized controlled trial. While the statistical association between discounts and losses is definitive, unobserved factors (customer price elasticity, product velocity, regional quotas) may confound direct causality.
2. **Absence of Customer Lifetime Value (CLV):** Isolated order profitability does not capture repeat purchase rates, referral value, or customer retention.
3. **Unobserved Fixed Costs:** Accounting profit in the dataset reflects gross margin minus allocable transaction expenses, omitting corporate overhead and supplier volume rebates.

---

## Project Structure

```
yuva-week3-statistical-analysis/
│
├── data/
│   ├── raw/
│   │   └── Sample - Superstore.csv            # Raw Superstore transactional dataset (9,994 rows)
│   └── processed/
│       └── superstore_cleaned.csv             # Cleaned dataset with engineered statistical features
│
├── notebooks/
│   └── week3_statistical_analysis.ipynb       # Fully executed Jupyter Notebook with all outputs & markdown
│
├── src/
│   ├── data_loading.py                        # Robust data ingestion with encoding fallbacks
│   ├── preprocessing.py                       # Data cleaning, validation, and feature engineering
│   ├── hypothesis_tests.py                    # Welch t-test, Mann-Whitney U, ANOVA, Chi-Square, Holm correction
│   ├── statistical_analysis.py                # Pipeline orchestrator and results table compiler
│   └── visualizations.py                      # 7 publication-standard statistical charts (300 DPI)
│
├── visualizations/
│   ├── 01_profit_distribution.png             # Histogram + KDE with skewness & kurtosis annotations
│   ├── 02_discount_vs_profit.png              # Scatter plot with regression trend line & disclaimer
│   ├── 03_group_comparison.png                # Box plot & violin plot of Discounted vs No Discount profit
│   ├── 04_category_profit_distribution.png    # Product category profit distributions
│   ├── 05_anova_comparison.png                # Category mean profit with 95% CIs & Tukey HSD brackets
│   ├── 06_contingency_heatmap.png             # Contingency heatmaps (counts & within-group proportions)
│   └── 07_confidence_intervals.png            # Forest plot of 95% confidence intervals
│
├── results/
│   └── statistical_results.csv                # Consolidated CSV results table
│
├── report/
│   └── YUVA_Week3_Statistical_Analysis_Report.docx  # Professional corporate/academic DOCX report
│
├── README.md                                  # Comprehensive project documentation
├── requirements.txt                           # Strict, minimal project dependencies
└── .gitignore                                 # Git configuration for Python & data artifacts
```

---

## How to Run

### **1. Environment Setup**
Ensure Python 3.10+ is installed. Clone the repository and initialize a virtual environment:

```bash
# Navigate to the project directory
cd yuva-week3-statistical-analysis

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### **2. Execute the Statistical Analysis Pipeline**
Run the end-to-end Python pipeline to process data, conduct all statistical tests, compile results, and generate all visualizations:

```bash
python src/statistical_analysis.py
```

### **3. Regenerate the Fully Executed Jupyter Notebook**
```bash
python ../build_notebook.py
```

### **4. Regenerate the Professional DOCX Report**
```bash
python ../build_docx_report.py
```

---

## Future Scope

1. **Econometric Causal Inference:** Implement Propensity Score Matching (PSM) and Instrumental Variable (IV) estimation to isolate true causal price elasticity from observational data.
2. **Randomized A/B Experimentation:** Design controlled promotional pricing experiments across randomized regional cohorts.
3. **Machine Learning Margin Prediction:** Train regularized regression models (Lasso/Ridge) and Gradient Boosted Trees (LightGBM/XGBoost) to predict profit elasticity across micro-segments.
4. **Customer-Level Longitudinal Tracking:** Aggregate transactional records to customer entities to evaluate multi-year Lifetime Value (CLV).

---

## Submission Checklist Verification

- [x] Public dataset selected and validated (Sample - Superstore.csv, N = 9,994).
- [x] Primary and secondary research questions defined.
- [x] Null ($H_0$) and alternative ($H_1$) hypotheses formally formulated.
- [x] Data cleaned, verified (0 missing values), and features engineered.
- [x] Descriptive statistics, skewness, and kurtosis computed.
- [x] Primary Welch's independent samples t-test conducted ($t = -15.7380, p < 0.001$).
- [x] Assumption checks conducted (normality, CLT applicability, Levene's homoscedasticity test).
- [x] Non-parametric Mann-Whitney U sensitivity test completed ($U = 6,266,805.5, p < 0.0001$).
- [x] One-Way ANOVA conducted ($F = 54.3110, p < 0.001, \eta^2 = 0.0108$).
- [x] Welch's robust ANOVA conducted ($F_W = 24.0825, p < 0.001$).
- [x] Tukey HSD post-hoc pairwise contrasts performed and analyzed.
- [x] Pearson's Chi-Square contingency test conducted ($\chi^2 = 2074.0898, p < 10^{-300}$).
- [x] Standardized effect sizes computed (Cohen's $d$, Eta squared, Cramer's $V$, Odds Ratio).
- [x] 95% confidence intervals estimated and interpreted with statistical precision.
- [x] Multiple testing correction applied (Holm-Bonferroni step-down).
- [x] 7 high-resolution statistical visualizations generated and saved.
- [x] Consolidated statistical results table exported to CSV (`results/statistical_results.csv`).
- [x] Professional, publication-grade DOCX report generated (`report/YUVA_Week3_Statistical_Analysis_Report.docx`).
- [x] Fully executed Jupyter Notebook generated (`notebooks/week3_statistical_analysis.ipynb`).
- [x] Complete project documentation (`README.md`), requirements (`requirements.txt`), and `.gitignore`.
