"""
Hypothesis Testing Module
YUVA Internship - Week 3

Implements rigorous parametric and non-parametric hypothesis tests:
- Welch's Two-Sample t-test (unequal variances)
- Mann-Whitney U test (non-parametric sensitivity check)
- One-Way ANOVA and Welch's ANOVA
- Tukey HSD Post-Hoc Analysis
- Pearson Chi-Square Contingency Test with Cramer's V
- Holm-Bonferroni Multiple Testing Correction
- Confidence Intervals and Effect Size Calculations
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from typing import Dict, Any, Tuple, List


def run_welch_ttest(
    group1: pd.Series,
    group2: pd.Series,
    group1_name: str = "Discounted",
    group2_name: str = "No Discount",
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Executes a two-sided Welch's independent samples t-test between two groups.
    Does NOT assume equal variances (equal_var=False).

    Returns comprehensive test results including sample statistics, t-statistic,
    Satterthwaite degrees of freedom, p-value, 95% confidence interval, and Cohen's d.
    """
    n1, n2 = len(group1), len(group2)
    m1, m2 = float(group1.mean()), float(group2.mean())
    med1, med2 = float(group1.median()), float(group2.median())
    s1, s2 = float(group1.std(ddof=1)), float(group2.std(ddof=1))
    v1, v2 = s1**2, s2**2

    mean_diff = m1 - m2

    # Welch t-statistic and p-value
    t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)

    # Welch-Satterthwaite degrees of freedom
    se_diff = np.sqrt(v1 / n1 + v2 / n2)
    df_welch = (v1 / n1 + v2 / n2)**2 / ((v1 / n1)**2 / (n1 - 1) + (v2 / n2)**2 / (n2 - 1))

    # 95% Confidence Interval for difference in means
    t_crit = stats.t.ppf(1 - alpha / 2, df_welch)
    ci_lower = mean_diff - t_crit * se_diff
    ci_upper = mean_diff + t_crit * se_diff

    # Pooled standard deviation & Cohen's d
    s_pooled = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    cohens_d = mean_diff / s_pooled
    # Hedges' g (sample-size bias-corrected Cohen's d)
    hedges_g = cohens_d * (1.0 - (3.0 / (4.0 * (n1 + n2) - 9.0)))

    # Levene test for equality of variance check
    lev_stat, lev_p = stats.levene(group1, group2)

    decision = "Reject H0" if p_val < alpha else "Fail to Reject H0"

    return {
        "test": "Welch's Independent Two-Sample t-test",
        "group1_name": group1_name,
        "group2_name": group2_name,
        "n1": n1,
        "n2": n2,
        "mean1": m1,
        "mean2": m2,
        "median1": med1,
        "median2": med2,
        "std1": s1,
        "std2": s2,
        "mean_diff": mean_diff,
        "se_diff": se_diff,
        "t_stat": float(t_stat),
        "df": float(df_welch),
        "p_value": float(p_val),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "cohens_d": float(cohens_d),
        "hedges_g": float(hedges_g),
        "levene_stat": float(lev_stat),
        "levene_p": float(lev_p),
        "alpha": alpha,
        "decision": decision
    }


def run_mann_whitney_test(
    group1: pd.Series,
    group2: pd.Series,
    group1_name: str = "Discounted",
    group2_name: str = "No Discount",
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Executes a two-sided Mann-Whitney U test as a non-parametric robustness check.
    """
    n1, n2 = len(group1), len(group2)
    u_stat, p_val = stats.mannwhitneyu(group1, group2, alternative="two-sided")
    # Rank-biserial correlation effect size r = 1 - (2*U / (n1 * n2))
    rank_biserial = 1.0 - (2.0 * u_stat / (n1 * n2))
    decision = "Reject H0" if p_val < alpha else "Fail to Reject H0"

    return {
        "test": "Mann-Whitney U Test (Robustness Check)",
        "group1_name": group1_name,
        "group2_name": group2_name,
        "n1": n1,
        "n2": n2,
        "u_stat": float(u_stat),
        "p_value": float(p_val),
        "rank_biserial_r": float(rank_biserial),
        "alpha": alpha,
        "decision": decision
    }


def run_one_way_anova(
    df: pd.DataFrame,
    group_col: str = "Category",
    val_col: str = "Profit",
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Executes a standard One-Way ANOVA across distinct levels of group_col.
    Also computes Levene's test and Eta squared effect size.
    """
    groups = [df[df[group_col] == cat][val_col].dropna() for cat in df[group_col].unique()]
    cat_names = df[group_col].unique().tolist()

    # Descriptive per category
    cat_stats = {}
    for cat in cat_names:
        sub = df[df[group_col] == cat][val_col].dropna()
        cat_stats[cat] = {
            "n": len(sub),
            "mean": float(sub.mean()),
            "median": float(sub.median()),
            "std": float(sub.std(ddof=1)),
            "ci_95": stats.t.interval(0.95, df=len(sub)-1, loc=sub.mean(), scale=stats.sem(sub))
        }

    # Levene test
    lev_stat, lev_p = stats.levene(*groups)

    # Standard ANOVA
    f_stat, p_val = stats.f_oneway(*groups)
    k = len(groups)
    n_total = len(df[val_col].dropna())
    df_between = k - 1
    df_within = n_total - k

    # Eta squared: SS_between / SS_total
    grand_mean = df[val_col].mean()
    ss_total = ((df[val_col] - grand_mean)**2).sum()
    ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
    eta_squared = ss_between / ss_total

    decision = "Reject H0" if p_val < alpha else "Fail to Reject H0"

    return {
        "test": "One-Way ANOVA",
        "group_col": group_col,
        "val_col": val_col,
        "categories": cat_names,
        "category_stats": cat_stats,
        "f_stat": float(f_stat),
        "df_between": df_between,
        "df_within": df_within,
        "p_value": float(p_val),
        "eta_squared": float(eta_squared),
        "levene_stat": float(lev_stat),
        "levene_p": float(lev_p),
        "alpha": alpha,
        "decision": decision
    }


def run_welch_anova(
    df: pd.DataFrame,
    group_col: str = "Category",
    val_col: str = "Profit",
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Executes Welch's ANOVA, which does not assume equal group variances.
    """
    groups = [df[df[group_col] == cat][val_col].dropna() for cat in df[group_col].unique()]
    k = len(groups)
    ni = np.array([len(g) for g in groups])
    mi = np.array([g.mean() for g in groups])
    vi = np.array([g.var(ddof=1) for g in groups])

    wi = ni / vi
    W = np.sum(wi)
    m_star = np.sum(wi * mi) / W

    ss_between_w = np.sum(wi * (mi - m_star)**2)
    q = (2.0 * (k - 2) / (k**2 - 1.0)) * np.sum(((1.0 - wi / W)**2) / (ni - 1.0))
    f_welch = ss_between_w / ((k - 1) * (1.0 + q))

    df1 = k - 1
    df2 = (k**2 - 1.0) / (3.0 * np.sum(((1.0 - wi / W)**2) / (ni - 1.0)))
    p_welch = 1.0 - stats.f.cdf(f_welch, df1, df2)

    decision = "Reject H0" if p_welch < alpha else "Fail to Reject H0"

    return {
        "test": "Welch's ANOVA (Robust Alternative)",
        "f_welch": float(f_welch),
        "df1": df1,
        "df2": float(df2),
        "p_value": float(p_welch),
        "alpha": alpha,
        "decision": decision
    }


def run_tukey_hsd(
    df: pd.DataFrame,
    group_col: str = "Category",
    val_col: str = "Profit",
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Executes Tukey's Honestly Significant Difference (HSD) post-hoc procedure.
    Controls Family-Wise Error Rate (FWER) across all pairwise comparisons.
    """
    tukey = pairwise_tukeyhsd(endog=df[val_col], groups=df[group_col], alpha=alpha)
    summary_df = pd.DataFrame(
        data=tukey._results_table.data[1:],
        columns=tukey._results_table.data[0]
    )
    return summary_df


def run_chi_square_test(
    df: pd.DataFrame,
    col1: str = "Discount_Status",
    col2: str = "Profitability_Status",
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Executes Pearson's Chi-Square Test of Independence on a 2x2 contingency table.
    Computes expected cell frequencies and Cramer's V effect size.
    """
    ct = pd.crosstab(df[col1], df[col2])
    chi2, p_val, dof, expected = stats.chi2_contingency(ct)

    n = ct.values.sum()
    min_dim = min(ct.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim))

    # Odds Ratio calculation for 2x2 table:
    # table layout:
    #                 Loss-making   Profitable
    # Discounted           a            b
    # No Discount          c            d
    # Odds of loss if discounted = (a/b) / (c/d) = (a*d)/(b*c)
    a = ct.loc['Discounted', 'Loss-making']
    b = ct.loc['Discounted', 'Profitable']
    c = ct.loc['No Discount', 'Loss-making']
    d = ct.loc['No Discount', 'Profitable']
    odds_ratio = (a * d) / (b * c) if (b * c) > 0 else np.nan

    min_expected = float(expected.min())
    decision = "Reject H0" if p_val < alpha else "Fail to Reject H0"

    return {
        "test": "Pearson's Chi-Square Test of Independence",
        "col1": col1,
        "col2": col2,
        "contingency_table": ct,
        "expected_frequencies": pd.DataFrame(expected, index=ct.index, columns=ct.columns),
        "chi2_stat": float(chi2),
        "df": int(dof),
        "p_value": float(p_val),
        "cramers_v": float(cramers_v),
        "odds_ratio": float(odds_ratio),
        "min_expected": min_expected,
        "alpha": alpha,
        "decision": decision
    }


def run_holm_bonferroni(p_dict: Dict[str, float], alpha: float = 0.05) -> pd.DataFrame:
    """
    Applies the Holm-Bonferroni step-down procedure to control Family-Wise Error Rate (FWER)
    across multiple hypothesis tests.
    """
    sorted_tests = sorted(p_dict.items(), key=lambda x: x[1])
    m = len(sorted_tests)
    results = []

    for rank, (test_name, raw_p) in enumerate(sorted_tests, 1):
        # Holm threshold: alpha / (m - rank + 1)
        holm_threshold = alpha / (m - rank + 1)
        adjusted_p = min(raw_p * (m - rank + 1), 1.0)
        results.append({
            "Rank": rank,
            "Test": test_name,
            "Raw p-value": raw_p,
            "Holm Threshold": holm_threshold,
            "Adjusted p-value": adjusted_p,
            "Significant (alpha=0.05)": "Yes (Reject H0)" if raw_p < holm_threshold else "No (Fail to Reject)"
        })

    # Ensure monotonicity of adjusted p-values
    df_holm = pd.DataFrame(results)
    for i in range(1, len(df_holm)):
        df_holm.loc[i, "Adjusted p-value"] = max(df_holm.loc[i, "Adjusted p-value"], df_holm.loc[i-1, "Adjusted p-value"])

    return df_holm


if __name__ == "__main__":
    from data_loading import load_raw_data
    from preprocessing import clean_and_prepare_data
    import os
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Sample - Superstore.csv")
    df = clean_and_prepare_data(load_raw_data(raw_path))
    res_t = run_welch_ttest(df[df['Discount_Status']=='Discounted']['Profit'], df[df['Discount_Status']=='No Discount']['Profit'])
    print("t-test p-value:", res_t['p_value'])
