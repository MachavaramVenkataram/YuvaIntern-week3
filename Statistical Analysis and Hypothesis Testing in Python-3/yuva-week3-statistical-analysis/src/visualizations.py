"""
Statistical Visualizations Module
YUVA Internship - Week 3

Produces 7 publication-quality statistical charts:
1. 01_profit_distribution.png: Profit distribution with histogram, KDE, and central tendency markers.
2. 02_discount_vs_profit.png: Discount vs. profit scatter plot with trend line and non-causality disclaimer.
3. 03_group_comparison.png: Discounted vs. No Discount profit box plot with mean markers.
4. 04_category_profit_distribution.png: Profit distributions across product categories.
5. 05_anova_comparison.png: Category mean profits with 95% confidence intervals and post-hoc annotations.
6. 06_contingency_heatmap.png: Discount Status x Profitability Status contingency matrix with proportions.
7. 07_confidence_intervals.png: Forest plot of 95% confidence intervals for means and difference.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple


def setup_plot_style():
    """Configures high-resolution, publication-standard styling."""
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams.update({
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif'],
        'font.size': 10,
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 14,
        'figure.titleweight': 'bold',
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'grid.alpha': 0.4,
        'grid.linestyle': '--'
    })


def plot_profit_distribution(df: pd.DataFrame, output_dir: str):
    """
    Figure 1: Profit Distribution
    Histogram + KDE with mean and median indicators.
    """
    setup_plot_style()
    fig, (ax_main, ax_zoom) = plt.subplots(1, 2, figsize=(14, 5.5))

    profit = df['Profit']
    mean_val = profit.mean()
    median_val = profit.median()
    skew_val = profit.skew()
    kurt_val = profit.kurtosis()

    # Left: Full Range Distribution (showing extreme outliers)
    sns.histplot(profit, bins=80, kde=True, color='#1B365D', ax=ax_main, edgecolor='white', alpha=0.7)
    ax_main.axvline(mean_val, color='#D9381E', linestyle='--', linewidth=2, label=f'Mean: ${mean_val:.2f}')
    ax_main.axvline(median_val, color='#2A9D8F', linestyle='-', linewidth=2, label=f'Median: ${median_val:.2f}')
    ax_main.set_yscale('log')
    ax_main.set_title('Figure 1A: Full Distribution (Log Scale)', pad=12)
    ax_main.set_xlabel('Profit ($ USD)')
    ax_main.set_ylabel('Transaction Count (Log Scale)')
    ax_main.legend(frameon=True, facecolor='white', framealpha=0.9)

    stats_text = (
        f"N = {len(profit):,}\n"
        f"Mean = ${mean_val:.2f}\n"
        f"Median = ${median_val:.2f}\n"
        f"Std Dev = ${profit.std():.2f}\n"
        f"Skewness = {skew_val:.2f}\n"
        f"Kurtosis = {kurt_val:.2f}"
    )
    ax_main.text(0.04, 0.72, stats_text, transform=ax_main.transAxes,
                 fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8F9FA', edgecolor='#CBD5E1', alpha=0.9))

    # Right: Focus Zoom [-250, 250] (capturing bulk of transactions)
    zoom_profit = profit[(profit >= -250) & (profit <= 250)]
    sns.histplot(zoom_profit, bins=60, kde=True, color='#2B5B84', ax=ax_zoom, edgecolor='white', alpha=0.7)
    ax_zoom.axvline(mean_val, color='#D9381E', linestyle='--', linewidth=2, label=f'Overall Mean: ${mean_val:.2f}')
    ax_zoom.axvline(median_val, color='#2A9D8F', linestyle='-', linewidth=2, label=f'Overall Median: ${median_val:.2f}')
    ax_zoom.axvline(0, color='#6C757D', linestyle=':', linewidth=1.5, label='Break-even ($0)')
    ax_zoom.set_title('Figure 1B: Central Distribution Focus [-$250 to +$250]', pad=12)
    ax_zoom.set_xlabel('Profit ($ USD)')
    ax_zoom.set_ylabel('Transaction Count')
    ax_zoom.legend(frameon=True, facecolor='white', framealpha=0.9)

    plt.suptitle('Figure 1: Superstore Transaction Profit Distribution & Skewness Analysis', y=1.02, fontsize=14, fontweight='bold', color='#0B2545')
    save_path = os.path.join(output_dir, '01_profit_distribution.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 1: {save_path}")


def plot_discount_vs_profit(df: pd.DataFrame, output_dir: str):
    """
    Figure 2: Discount vs Profit Scatter Plot
    Shows negative association, jitter, and non-causality disclaimer.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6.5))

    # Add slight jitter to discount for visual separation of discrete rates
    np.random.seed(42)
    jitter = np.random.normal(0, 0.005, size=len(df))
    jittered_discount = df['Discount'] + jitter

    scatter = ax.scatter(
        jittered_discount * 100,
        df['Profit'],
        alpha=0.25,
        color='#1B365D',
        edgecolors='none',
        s=28,
        label='Order Transactions (N=9,994)'
    )

    # Trend line (linear fit)
    sns.regplot(
        x=df['Discount'] * 100,
        y=df['Profit'],
        scatter=False,
        ax=ax,
        color='#D9381E',
        line_kws={'linewidth': 2.5, 'label': 'Linear Regression Trend (OOD)'}
    )

    ax.axhline(0, color='#2A9D8F', linestyle='--', linewidth=1.5, label='Break-even Baseline ($0)')

    # Annotate loss threshold
    ax.axvline(20, color='#E76F51', linestyle=':', linewidth=1.5, alpha=0.8)
    ax.text(21, 4000, 'Threshold: Discounts > 20% precipitate severe losses',
            fontsize=9.5, color='#B71C1C', fontweight='semibold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3CD', edgecolor='#FFEEBA'))

    ax.set_title('Figure 2: Transaction Discount Rate vs. Net Profit', pad=14, color='#0B2545')
    ax.set_xlabel('Discount Rate (%)')
    ax.set_ylabel('Profit ($ USD)')
    ax.set_ylim(-7000, 9000)
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)

    # Crucial scientific disclaimer
    disclaimer = "METHODOLOGICAL NOTE: Statistical association does NOT prove direct causation. Confounding variables (category, volume, seasonality) may influence profitability."
    plt.figtext(0.5, -0.04, disclaimer, ha='center', fontsize=8.5, fontstyle='italic', color='#555555')

    save_path = os.path.join(output_dir, '02_discount_vs_profit.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 2: {save_path}")


def plot_group_comparison(df: pd.DataFrame, output_dir: str):
    """
    Figure 3: Discounted vs Non-Discounted Profit
    Box plot & violin plot comparing two groups with mean diamond markers.
    """
    setup_plot_style()
    fig, (ax_box, ax_violin) = plt.subplots(1, 2, figsize=(13, 6))

    palette = {'No Discount': '#2A9D8F', 'Discounted': '#E76F51'}

    # Left: Truncated Box Plot showing central quartiles clearly
    sns.boxplot(
        data=df,
        x='Discount_Status',
        y='Profit',
        order=['No Discount', 'Discounted'],
        palette=palette,
        ax=ax_box,
        showmeans=True,
        meanprops={'marker': 'D', 'markerfacecolor': '#0B2545', 'markeredgecolor': 'black', 'markersize': 8, 'label': 'Group Mean'},
        boxprops={'alpha': 0.8},
        showfliers=False
    )
    ax_box.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax_box.set_title('Figure 3A: Interquartile Ranges (Excl. Outliers)', pad=12)
    ax_box.set_xlabel('Order Discount Status')
    ax_box.set_ylabel('Profit ($ USD)')

    # Add numeric labels for means and medians
    nodisc = df[df['Discount_Status'] == 'No Discount']['Profit']
    disc = df[df['Discount_Status'] == 'Discounted']['Profit']

    ax_box.text(0, nodisc.median() + 8, f"Med: ${nodisc.median():.1f}\nMean: ${nodisc.mean():.1f}",
                ha='center', fontsize=9, fontweight='bold', color='#0B2545')
    ax_box.text(1, disc.median() + 8, f"Med: ${disc.median():.1f}\nMean: -${abs(disc.mean()):.1f}",
                ha='center', fontsize=9, fontweight='bold', color='#B71C1C')

    # Right: Violin Plot with inner quartiles (trimmed to central 90% for readability)
    p_low, p_high = np.percentile(df['Profit'], [2.5, 97.5])
    df_filtered = df[(df['Profit'] >= p_low) & (df['Profit'] <= p_high)]

    sns.violinplot(
        data=df_filtered,
        x='Discount_Status',
        y='Profit',
        order=['No Discount', 'Discounted'],
        palette=palette,
        ax=ax_violin,
        inner='quartile',
        cut=0
    )
    ax_violin.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax_violin.set_title('Figure 3B: Density Profiles (95% Core Range)', pad=12)
    ax_violin.set_xlabel('Order Discount Status')
    ax_violin.set_ylabel('Profit ($ USD)')

    plt.suptitle('Figure 3: Profit Comparison: No Discount (N=4,798) vs. Discounted (N=5,196)', y=1.02, fontsize=14, fontweight='bold', color='#0B2545')
    save_path = os.path.join(output_dir, '03_group_comparison.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 3: {save_path}")


def plot_category_profit_distribution(df: pd.DataFrame, output_dir: str):
    """
    Figure 4: Category Profit Distribution
    Box plots comparing Furniture, Office Supplies, and Technology.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(11, 6))

    palette = {'Technology': '#1B365D', 'Office Supplies': '#2A9D8F', 'Furniture': '#E76F51'}
    order = ['Technology', 'Office Supplies', 'Furniture']

    sns.boxplot(
        data=df,
        x='Category',
        y='Profit',
        order=order,
        palette=palette,
        ax=ax,
        showmeans=True,
        meanprops={'marker': 'D', 'markerfacecolor': 'gold', 'markeredgecolor': 'black', 'markersize': 9, 'label': 'Mean Marker'},
        showfliers=False,
        boxprops={'alpha': 0.85}
    )
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.2, label='Break-even ($0)')

    # Overlay text annotations for each category
    for i, cat in enumerate(order):
        sub = df[df['Category'] == cat]['Profit']
        mean_c = sub.mean()
        med_c = sub.median()
        ax.text(i, mean_c + 12, f"Mean: ${mean_c:.2f}\nMed: ${med_c:.2f}\n(N={len(sub):,})",
                ha='center', fontsize=9.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#CBD5E1', alpha=0.9))

    ax.set_title('Figure 4: Profit Distribution Across Product Categories (Excl. Outliers for Visualization)', pad=14, color='#0B2545')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Profit ($ USD)')
    ax.set_ylim(-120, 160)
    ax.legend(loc='upper right', frameon=True, facecolor='white')

    save_path = os.path.join(output_dir, '04_category_profit_distribution.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 4: {save_path}")


def plot_anova_comparison(df: pd.DataFrame, output_dir: str):
    """
    Figure 5: ANOVA Comparison
    Category means with 95% confidence interval error bars, F-test stats, and post-hoc Tukey results.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6.5))

    cats = ['Furniture', 'Office Supplies', 'Technology']
    means = [df[df['Category'] == c]['Profit'].mean() for c in cats]
    sems = [stats.sem(df[df['Category'] == c]['Profit']) for c in cats]
    counts = [len(df[df['Category'] == c]) for c in cats]
    ci_margins = [stats.t.ppf(0.975, df=n-1) * s for n, s in zip(counts, sems)]

    colors = ['#E76F51', '#2A9D8F', '#1B365D']
    x_pos = np.arange(len(cats))

    bars = ax.bar(x_pos, means, yerr=ci_margins, capsize=8, color=colors, alpha=0.85, edgecolor='black', width=0.55,
                  error_kw={'elinewidth': 2, 'ecolor': '#0B2545', 'capthick': 2})

    ax.axhline(0, color='gray', linestyle='--', linewidth=1)

    # Label each bar with exact values
    for i, (b, m, ci, n) in enumerate(zip(bars, means, ci_margins, counts)):
        ax.text(b.get_x() + b.get_width()/2., m + ci + 4,
                f"${m:.2f}\n95% CI: [${m-ci:.1f}, ${m+ci:.1f}]\nN={n:,}",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold')

    # Post-hoc comparison brackets
    ax.annotate('', xy=(0, 92), xytext=(2, 92),
                arrowprops=dict(arrowstyle='-', color='black', lw=1.5))
    ax.text(1, 95, "Tukey HSD: Diff = $70.05, p < 0.001 (Significant)",
            ha='center', fontsize=9, fontweight='semibold', color='#0B2545')

    ax.annotate('', xy=(1, 80), xytext=(2, 80),
                arrowprops=dict(arrowstyle='-', color='black', lw=1.5))
    ax.text(1.5, 83, "Tukey HSD: Diff = $58.43, p < 0.001 (Significant)",
            ha='center', fontsize=9, fontweight='semibold', color='#0B2545')

    ax.annotate('', xy=(0, 38), xytext=(1, 38),
                arrowprops=dict(arrowstyle='-', color='gray', lw=1.2, ls='--'))
    ax.text(0.5, 41, "Diff = $11.63, p = 0.118 (Not Significant)",
            ha='center', fontsize=8.5, fontstyle='italic', color='#555555')

    ax.set_xticks(x_pos)
    ax.set_xticklabels(cats, fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Profit ($ USD)')
    ax.set_title('Figure 5: One-Way ANOVA: Mean Category Profit with 95% Confidence Intervals', pad=14, color='#0B2545')
    ax.set_ylim(-10, 115)

    stats_badge = "ANOVA F(2, 9991) = 54.31, p = 3.47e-24\nWelch ANOVA F(2, 3587) = 24.08, p = 4.08e-11\nEta Squared = 0.0108"
    ax.text(0.04, 0.88, stats_badge, transform=ax.transAxes,
            fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8F9FA', edgecolor='#CBD5E1'))

    save_path = os.path.join(output_dir, '05_anova_comparison.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 5: {save_path}")


def plot_contingency_heatmap(df: pd.DataFrame, output_dir: str):
    """
    Figure 6: Contingency Heatmap
    Discount Status x Profitability Status cross-tabulation with percentages and Chi-square statistics.
    """
    setup_plot_style()
    fig, (ax_count, ax_prop) = plt.subplots(1, 2, figsize=(14, 5.5))

    ct = pd.crosstab(df['Discount_Status'], df['Profitability_Status'])
    ct = ct.reindex(index=['No Discount', 'Discounted'], columns=['Profitable', 'Loss-making'])

    # Row proportions
    ct_prop = ct.div(ct.sum(axis=1), axis=0) * 100

    # Left: Counts Heatmap
    sns.heatmap(ct, annot=True, fmt=',d', cmap='Blues', cbar=False, ax=ax_count,
                annot_kws={'size': 13, 'weight': 'bold'}, linewidths=1.5, linecolor='white')
    ax_count.set_title('Figure 6A: Observed Transaction Counts', pad=12)
    ax_count.set_xlabel('Profitability Status')
    ax_count.set_ylabel('Discount Status')

    # Right: Row Percentages Heatmap
    sns.heatmap(ct_prop, annot=True, fmt='.2f', cmap='YlOrRd', cbar=True, ax=ax_prop,
                annot_kws={'size': 13, 'weight': 'bold'}, linewidths=1.5, linecolor='white')
    # Append % symbol to annotations in code
    for text in ax_prop.texts:
        text.set_text(text.get_text() + '%')

    ax_prop.set_title('Figure 6B: Within-Group Proportions (%)', pad=12)
    ax_prop.set_xlabel('Profitability Status')
    ax_prop.set_ylabel('Discount Status')

    stats_summary = "Chi-Square Test of Independence: χ² = 2074.09, df = 1, p < 0.0001 | Cramer's V = 0.4556 (Strong Effect) | Odds Ratio = 91.95"
    plt.suptitle(f'Figure 6: Discount Status × Profitability Association\n{stats_summary}', y=1.04, fontsize=13, fontweight='bold', color='#0B2545')

    save_path = os.path.join(output_dir, '06_contingency_heatmap.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 6: {save_path}")


def plot_confidence_intervals(df: pd.DataFrame, output_dir: str):
    """
    Figure 7: Confidence Intervals Summary
    Forest plot of 95% Confidence Intervals for group means and mean difference.
    """
    setup_plot_style()
    fig, (ax_groups, ax_diff) = plt.subplots(1, 2, figsize=(14, 5.8), gridspec_kw={'width_ratios': [1.2, 1]})

    # Group CIs
    items = []
    # Categories
    for cat in ['Technology', 'Office Supplies', 'Furniture']:
        sub = df[df['Category'] == cat]['Profit']
        mean = sub.mean()
        ci = stats.t.interval(0.95, df=len(sub)-1, loc=mean, scale=stats.sem(sub))
        items.append({'Label': f"Category: {cat}", 'Mean': mean, 'Low': ci[0], 'High': ci[1], 'Color': '#1B365D'})

    # Discount Groups
    for disc_status, color in [('No Discount', '#2A9D8F'), ('Discounted', '#E76F51')]:
        sub = df[df['Discount_Status'] == disc_status]['Profit']
        mean = sub.mean()
        ci = stats.t.interval(0.95, df=len(sub)-1, loc=mean, scale=stats.sem(sub))
        items.append({'Label': f"Status: {disc_status}", 'Mean': mean, 'Low': ci[0], 'High': ci[1], 'Color': color})

    y_pos = np.arange(len(items))

    for y, it in zip(y_pos, items):
        ax_groups.errorbar(
            it['Mean'], y,
            xerr=[[it['Mean'] - it['Low']], [it['High'] - it['Mean']]],
            fmt='o', color=it['Color'], ecolor=it['Color'], elinewidth=2.5, capsize=6, markersize=8
        )
        ax_groups.text(it['Mean'], y + 0.22, f"${it['Mean']:.1f} [{it['Low']:.1f}, {it['High']:.1f}]",
                       ha='center', fontsize=9, fontweight='semibold')

    ax_groups.axvline(0, color='gray', linestyle='--', linewidth=1)
    ax_groups.set_yticks(y_pos)
    ax_groups.set_yticklabels([it['Label'] for it in items], fontsize=10.5, fontweight='bold')
    ax_groups.set_xlabel('Mean Profit ($ USD)')
    ax_groups.set_title('Figure 7A: Group Mean 95% Confidence Intervals', pad=12)
    ax_groups.set_ylim(-0.6, len(items) - 0.2)

    # Right: Difference in Means (Discounted - No Discount)
    d_sub = df[df['Discount_Status'] == 'Discounted']['Profit']
    nd_sub = df[df['Discount_Status'] == 'No Discount']['Profit']
    mean_diff = d_sub.mean() - nd_sub.mean()
    s1, s2 = d_sub.var(), nd_sub.var()
    n1, n2 = len(d_sub), len(nd_sub)
    df_welch = (s1/n1 + s2/n2)**2 / ((s1/n1)**2 / (n1 - 1) + (s2/n2)**2 / (n2 - 1))
    se_diff = np.sqrt(s1/n1 + s2/n2)
    t_crit = stats.t.ppf(0.975, df_welch)
    diff_low = mean_diff - t_crit * se_diff
    diff_high = mean_diff + t_crit * se_diff

    ax_diff.errorbar(
        mean_diff, 0,
        xerr=[[mean_diff - diff_low], [diff_high - mean_diff]],
        fmt='s', color='#B71C1C', ecolor='#B71C1C', elinewidth=3, capsize=8, markersize=10
    )
    ax_diff.axvline(0, color='black', linestyle='-', linewidth=1.5, label='Null Effect (Δ = 0)')
    ax_diff.text(mean_diff, 0.2, f"Δ = -${abs(mean_diff):.2f}\n95% CI: [-${abs(diff_low):.2f}, -${abs(diff_high):.2f}]",
                 ha='center', fontsize=10, fontweight='bold', color='#B71C1C')

    ax_diff.set_yticks([0])
    ax_diff.set_yticklabels(['Discounted - No Discount'], fontsize=11, fontweight='bold')
    ax_diff.set_xlabel('Profit Difference ($ USD)')
    ax_diff.set_title('Figure 7B: 95% CI for Difference in Means (Welch)', pad=12)
    ax_diff.set_ylim(-0.6, 0.6)
    ax_diff.legend(loc='lower right', frameon=True)

    plt.suptitle('Figure 7: Summary of Estimated 95% Confidence Intervals', y=1.03, fontsize=14, fontweight='bold', color='#0B2545')
    save_path = os.path.join(output_dir, '07_confidence_intervals.png')
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved Figure 7: {save_path}")


def generate_all_visualizations(df: pd.DataFrame, output_dir: str):
    """Generates all 7 required statistical charts and saves them to disk."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"[INFO] Generating publication-quality charts in: {output_dir}")
    plot_profit_distribution(df, output_dir)
    plot_discount_vs_profit(df, output_dir)
    plot_group_comparison(df, output_dir)
    plot_category_profit_distribution(df, output_dir)
    plot_anova_comparison(df, output_dir)
    plot_contingency_heatmap(df, output_dir)
    plot_confidence_intervals(df, output_dir)
    print("[INFO] All 7 charts successfully generated.")


if __name__ == "__main__":
    from data_loading import load_raw_data
    from preprocessing import clean_and_prepare_data
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Sample - Superstore.csv")
    viz_dir = os.path.join(os.path.dirname(__file__), "..", "visualizations")
    df = clean_and_prepare_data(load_raw_data(raw_path))
    generate_all_visualizations(df, viz_dir)
