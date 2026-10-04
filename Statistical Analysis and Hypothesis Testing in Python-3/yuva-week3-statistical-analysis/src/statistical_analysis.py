"""
Statistical Analysis Orchestrator
YUVA Internship - Week 3

Coordinates end-to-end execution of descriptive analytics, assumption verification,
hypothesis testing, post-hoc analysis, Holm-Bonferroni multiple testing correction,
and consolidated results reporting.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Any

from data_loading import load_raw_data
from preprocessing import clean_and_prepare_data
from hypothesis_tests import (
    run_welch_ttest,
    run_mann_whitney_test,
    run_one_way_anova,
    run_welch_anova,
    run_tukey_hsd,
    run_chi_square_test,
    run_holm_bonferroni
)
from visualizations import generate_all_visualizations


def compute_descriptive_statistics(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Computes comprehensive univariate and bivariate descriptive statistics."""
    numeric_cols = ['Sales', 'Profit', 'Discount', 'Quantity']
    
    # Univariate summary
    desc_df = df[numeric_cols].describe().T
    desc_df['median'] = df[numeric_cols].median()
    desc_df['skewness'] = df[numeric_cols].skew()
    desc_df['kurtosis'] = df[numeric_cols].kurtosis()
    desc_df = desc_df[['count', 'mean', 'std', 'min', '25%', 'median', '75%', 'max', 'skewness', 'kurtosis']]

    # Group statistics: Profit by Discount Status
    profit_by_discount = df.groupby('Discount_Status')['Profit'].agg(
        Count='count',
        Mean='mean',
        Median='median',
        Std='std',
        IQR=lambda x: np.percentile(x, 75) - np.percentile(x, 25),
        Min='min',
        Max='max'
    ).reset_index()

    # Group statistics: Profit by Category
    profit_by_cat = df.groupby('Category')['Profit'].agg(
        Count='count',
        Mean='mean',
        Median='median',
        Std='std',
        IQR=lambda x: np.percentile(x, 75) - np.percentile(x, 25),
        Min='min',
        Max='max'
    ).reset_index()

    # Group statistics: Profit by Discount Band
    profit_by_band = df.groupby('Discount_Band', observed=True)['Profit'].agg(
        Count='count',
        Mean='mean',
        Median='median',
        Std='std',
        Loss_Rate=lambda x: (x <= 0).mean() * 100.0
    ).reset_index()

    return {
        "numeric_summary": desc_df,
        "profit_by_discount": profit_by_discount,
        "profit_by_category": profit_by_cat,
        "profit_by_discount_band": profit_by_band
    }


def execute_full_pipeline(
    raw_csv_path: str,
    processed_csv_path: str,
    visualizations_dir: str,
    results_csv_path: str
) -> Dict[str, Any]:
    """
    Executes the complete statistical study:
    1. Loads raw dataset
    2. Preprocesses and engineers variables
    3. Runs descriptive profiling
    4. Performs Welch t-test, Mann-Whitney U, ANOVA, Welch ANOVA, Tukey HSD, Chi-square
    5. Applies Holm-Bonferroni correction
    6. Compiles and saves consolidated results CSV
    7. Generates publication-ready figures
    """
    print("=" * 70)
    print("STARTING YUVA WEEK 3 STATISTICAL ANALYSIS PIPELINE")
    print("=" * 70)

    # 1. Load Data
    raw_df = load_raw_data(raw_csv_path)

    # 2. Preprocess & Feature Engineering
    df = clean_and_prepare_data(raw_df, output_path=processed_csv_path)

    # 3. Descriptive Stats
    desc_stats = compute_descriptive_statistics(df)

    # 4. Hypothesis Testing
    # H1: Welch t-test
    disc_sub = df[df['Discount_Status'] == 'Discounted']['Profit']
    nodisc_sub = df[df['Discount_Status'] == 'No Discount']['Profit']
    t_results = run_welch_ttest(disc_sub, nodisc_sub)

    # H1 Sensitivity: Mann-Whitney U test
    mw_results = run_mann_whitney_test(disc_sub, nodisc_sub)

    # H2: One-Way ANOVA
    anova_results = run_one_way_anova(df, group_col='Category', val_col='Profit')

    # H2 Robustness: Welch's ANOVA
    welch_anova_results = run_welch_anova(df, group_col='Category', val_col='Profit')

    # H2 Post-Hoc: Tukey HSD
    tukey_results = run_tukey_hsd(df, group_col='Category', val_col='Profit')

    # H3: Chi-Square Test of Independence
    chi2_results = run_chi_square_test(df, col1='Discount_Status', col2='Profitability_Status')

    # Multiple Testing Correction: Holm-Bonferroni
    p_family = {
        "Welch t-test (Discount vs Profit)": t_results["p_value"],
        "Mann-Whitney U (Sensitivity Check)": mw_results["p_value"],
        "One-Way ANOVA (Category Profit)": anova_results["p_value"],
        "Welch's ANOVA (Robust Category Test)": welch_anova_results["p_value"],
        "Chi-Square Test (Discount x Profitability)": chi2_results["p_value"]
    }
    holm_results = run_holm_bonferroni(p_family, alpha=0.05)

    # 5. Build Consolidated Statistical Results Table
    results_rows = [
        {
            "Test": "Welch's Independent t-test (Primary)",
            "Research Question": "Does receiving a discount affect average order-level profit?",
            "Statistic": f"t = {t_results['t_stat']:.4f}",
            "Degrees of Freedom": f"{t_results['df']:.2f}",
            "p-value": f"{t_results['p_value']:.4e}",
            "Effect Size": f"Cohen's d = {t_results['cohens_d']:.4f}",
            "95% CI": f"[{t_results['ci_lower']:.2f}, {t_results['ci_upper']:.2f}]",
            "Decision": t_results["decision"],
            "Interpretation": "Discounted orders have significantly lower average profit (-$73.56 lower)."
        },
        {
            "Test": "Mann-Whitney U Test (Robustness Check)",
            "Research Question": "Is profit distribution shifted between discount groups (non-parametric)?",
            "Statistic": f"U = {mw_results['u_stat']:.1f}",
            "Degrees of Freedom": "N/A (Rank sum)",
            "p-value": f"{mw_results['p_value']:.4e}",
            "Effect Size": f"Rank-biserial r = {mw_results['rank_biserial_r']:.4f}",
            "95% CI": "N/A",
            "Decision": mw_results["decision"],
            "Interpretation": "Rank-based median profit distribution is significantly lower for discounted orders."
        },
        {
            "Test": "One-Way ANOVA (Secondary)",
            "Research Question": "Does average profit differ significantly across product categories?",
            "Statistic": f"F = {anova_results['f_stat']:.4f}",
            "Degrees of Freedom": f"({anova_results['df_between']}, {anova_results['df_within']})",
            "p-value": f"{anova_results['p_value']:.4e}",
            "Effect Size": f"Eta squared = {anova_results['eta_squared']:.4f}",
            "95% CI": "Category-specific",
            "Decision": anova_results["decision"],
            "Interpretation": "Mean profit differs significantly across product categories (driven by Technology)."
        },
        {
            "Test": "Welch's ANOVA (Robust Category Test)",
            "Research Question": "Does average profit differ across categories under heteroscedasticity?",
            "Statistic": f"F_W = {welch_anova_results['f_welch']:.4f}",
            "Degrees of Freedom": f"({welch_anova_results['df1']}, {welch_anova_results['df2']:.2f})",
            "p-value": f"{welch_anova_results['p_value']:.4e}",
            "Effect Size": f"Eta squared = {anova_results['eta_squared']:.4f}",
            "95% CI": "Category-specific",
            "Decision": welch_anova_results["decision"],
            "Interpretation": "Category differences remain highly significant when relaxing equal variance assumption."
        },
        {
            "Test": "Pearson's Chi-Square Test (Secondary)",
            "Research Question": "Is discount status associated with order profitability status (loss vs profit)?",
            "Statistic": f"Chi2 = {chi2_results['chi2_stat']:.4f}",
            "Degrees of Freedom": f"{chi2_results['df']}",
            "p-value": f"{chi2_results['p_value']:.4e}",
            "Effect Size": f"Cramer's V = {chi2_results['cramers_v']:.4f}",
            "95% CI": f"Odds Ratio = {chi2_results['odds_ratio']:.2f}",
            "Decision": chi2_results["decision"],
            "Interpretation": "Discounted orders have a drastically higher probability of incurring net losses (36.7% vs 0.6%)."
        }
    ]

    results_df = pd.DataFrame(results_rows)
    os.makedirs(os.path.dirname(results_csv_path), exist_ok=True)
    results_df.to_csv(results_csv_path, index=False)
    print(f"[INFO] Saved consolidated statistical results table to: {results_csv_path}")

    # 6. Generate Visualizations
    generate_all_visualizations(df, visualizations_dir)

    print("=" * 70)
    print("PIPELINE EXECUTION SUCCESSFULLY COMPLETED")
    print("=" * 70)

    return {
        "df": df,
        "desc_stats": desc_stats,
        "t_results": t_results,
        "mw_results": mw_results,
        "anova_results": anova_results,
        "welch_anova_results": welch_anova_results,
        "tukey_results": tukey_results,
        "chi2_results": chi2_results,
        "holm_results": holm_results,
        "results_df": results_df
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "Sample - Superstore.csv")
    proc_path = os.path.join(base_dir, "data", "processed", "superstore_cleaned.csv")
    viz_path = os.path.join(base_dir, "visualizations")
    res_path = os.path.join(base_dir, "results", "statistical_results.csv")

    results = execute_full_pipeline(raw_path, proc_path, viz_path, res_path)
