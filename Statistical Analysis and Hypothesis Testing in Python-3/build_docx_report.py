"""
DOCX Report Builder for YUVA Internship - Week 3
Statistical Analysis and Hypothesis Testing in Python

Generates a publication-grade corporate/academic DOCX report:
- Custom typography, hierarchy, and executive color palette (Navy, Slate, Gold, Crisp White)
- Styled Title Page with formal institutional branding
- 19 structured sections addressing all prompt requirements
- Clean statistical summary tables with cell shading and borders
- Embedded high-resolution figures with complete 5-part analytical breakdowns
- Formatted monospace code snippets with grey container shading
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


# Color constants
COLOR_NAVY = RGBColor(11, 37, 69)       # Primary Title/Heading (#0B2545)
COLOR_STEEL = RGBColor(27, 54, 93)      # Secondary Heading (#1B365D)
COLOR_SLATE = RGBColor(51, 65, 85)      # Body Dark Slate (#334155)
COLOR_MUTED = RGBColor(100, 116, 139)   # Captions/Muted (#64748B)
COLOR_CRIMSON = RGBColor(183, 28, 28)   # Alert/Negative (#B71C1C)
COLOR_TEAL = RGBColor(42, 157, 143)     # Positive (#2A9D8F)
HEX_NAVY = "0B2545"
HEX_LIGHT_BLUE = "F0F4F8"
HEX_ZEBRA = "F8FAFC"
HEX_CODE_BG = "F1F5F9"
HEX_BORDER = "CBD5E1"


def set_cell_background(cell, hex_color: str):
    """Sets background shading of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding (in twips) of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Applies clean, subtle borders to all cells in a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="none"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)


def format_table(table, col_widths, headers, data, align_rights=[]):
    """Standardizes styling across all statistical summary tables."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color=HEX_BORDER, sz="6")

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=140, bottom=140, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if i in align_rights else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in align_rights else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(9)
                run.font.color.rgb = COLOR_SLATE

    # Column widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width


def add_code_block(doc, code_str: str):
    """Inserts a styled, bordered monospace code container."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, HEX_CODE_BG)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    # Left border highlight
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_NAVY}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_str.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def add_callout(doc, text: str, title: str = "KEY STATISTICAL INSIGHT"):
    """Inserts a highlighted callout box for core findings."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, HEX_LIGHT_BLUE)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="28" w:space="0" w:color="0B2545"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"[{title}] ")
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(9.5)
    run_t.font.bold = True
    run_t.font.color.rgb = COLOR_NAVY

    run_body = p.add_run(text)
    run_body.font.name = 'Arial'
    run_body.font.size = Pt(9.5)
    run_body.font.italic = True
    run_body.font.color.rgb = COLOR_SLATE
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def add_heading_1(doc, text: str):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return h


def add_heading_2(doc, text: str):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_STEEL
    return h


def add_heading_3(doc, text: str):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_SLATE
    return h


def add_body_p(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_SLATE
    return p


def build_docx_report(output_docx_path: str, viz_dir: str):
    """Assembles and writes the comprehensive Week 3 internship report."""
    print("=" * 70)
    print("BUILDING PROFESSIONAL DOCX INTERNSHIP REPORT")
    print("=" * 70)

    doc = docx.Document()

    # Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # TITLE PAGE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(40)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_org = title_p.add_run("YUVA INTERNSHIP PROGRAM")
    run_org.font.name = 'Arial'
    run_org.font.size = Pt(14)
    run_org.font.bold = True
    run_org.font.color.rgb = COLOR_MUTED

    sub_org = doc.add_paragraph()
    sub_org.paragraph_format.space_before = Pt(0)
    sub_org.paragraph_format.space_after = Pt(24)
    sub_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_org.add_run("DATA SCIENCE & APPLIED ANALYTICS TRACK -- WEEK 3 TASK")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_STEEL

    # Main Project Title
    p_main = doc.add_paragraph()
    p_main.paragraph_format.space_before = Pt(10)
    p_main.paragraph_format.space_after = Pt(8)
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_main = p_main.add_run("STATISTICAL ANALYSIS AND\nHYPOTHESIS TESTING IN PYTHON")
    r_main.font.name = 'Arial'
    r_main.font.size = Pt(22)
    r_main.font.bold = True
    r_main.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(36)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run('"Statistical Investigation of Sales, Discounts, and Profitability in Superstore Data"')
    r_sub.font.name = 'Georgia'
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_SLATE

    # Metadata Card (Table layout)
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="FFFFFF", sz="0")
    
    meta_data = [
        ("Prepared By:", "YUVA Data Science Intern"),
        ("Project Scope:", "Enterprise Inferential Statistics & Hypothesis Testing"),
        ("Technology Stack:", "Python 3.13 | Pandas | SciPy | Statsmodels | Seaborn"),
        ("Dataset Evaluated:", "Retail Superstore Sales Dataset (N = 9,994 transactions)"),
        ("Submission Date:", "October 2026")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.0)
        
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.paragraph_format.space_before = Pt(3)
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(label)
        r0.font.name = 'Arial'
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY

        p1 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_before = Pt(3)
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(val)
        r1.font.name = 'Arial'
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_SLATE

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    add_heading_1(doc, "1. Executive Summary")
    add_body_p(doc, 
        "This project delivers an enterprise-grade inferential statistical investigation into retail commercial performance, "
        "evaluating the empirical relationship between promotional discounting, merchandise category, and order-level net profitability. "
        "Using a complete observational sample of 9,994 transactions from the Superstore retail enterprise, we test explicit business "
        "hypotheses using rigorous parametric and non-parametric testing procedures at a two-sided significance threshold of alpha = 0.05."
    )
    add_body_p(doc, 
        "Our primary hypothesis test confirms that promotional discounts exert a profound, statistically significant negative effect on "
        "transaction profitability. Non-discounted transactions (N = 4,798) achieve an average profit of +$66.90 (median +$15.99), "
        "whereas discounted transactions (N = 5,196) incur an average net loss of -$6.66 (median +$3.34). A Welch's independent samples "
        "t-test reveals an estimated mean difference of -$73.56 (t = -15.7380, p = 4.36e-55), with a 95% confidence interval of "
        "[-$82.72, -$64.40] and a standardized effect size of Cohen's d = -0.3179. A non-parametric Mann-Whitney U robustness check "
        "corroborates this finding (U = 6,266,805.5, p < 0.0001, rank-biserial r = 0.4973), demonstrating that the profit decline is "
        "structurally genuine and not an artifact of distributional skewness."
    )
    add_body_p(doc, 
        "Secondary testing via One-Way ANOVA indicates significant profit variation across merchandise categories (F = 54.3110, p = 3.47e-24, "
        "eta^2 = 0.0108), validated under heteroscedasticity via Welch's robust ANOVA (F_W = 24.0825, p = 4.08e-11). Post-hoc Tukey HSD "
        "contrasts establish that Technology delivers significantly higher mean profit ($78.75) than Office Supplies ($20.33) and Furniture ($8.70), "
        "while Furniture and Office Supplies do not significantly differ from one another (p_adj = 0.1181). Furthermore, a Pearson Chi-Square test "
        "of independence establishes a stark association between discounting and order loss incidence (Chi2 = 2074.0898, df = 1, p < 1e-300, "
        "Cramer's V = 0.4556). Whereas non-discounted orders exhibit a near-zero loss rate (0.63%), discounted orders incur losses in 36.68% of cases, "
        "translating to an Odds Ratio of 91.95. Management is strongly advised to enforce a maximum promotional discount cap of 20% and abolish "
        "unfettered discounting in low-margin categories like Furniture."
    )

    add_callout(doc, 
        "Discounted transactions suffer a -$73.56 lower mean profit (t = -15.738, p < 0.001, 95% CI: [-$82.72, -$64.40]) and carry nearly "
        "92-fold higher odds of incurring a net financial loss (36.68% vs. 0.63%). Discounting represents the single largest structural margin drain in the enterprise.",
        "EXECUTIVE TAKEAWAY"
    )

    # -------------------------------------------------------------
    # 2. INTRODUCTION
    # -------------------------------------------------------------
    add_heading_1(doc, "2. Introduction")
    add_body_p(doc, 
        "In modern commercial retail, promotional discounting is conventionally treated as an indispensable lever for top-line revenue expansion, "
        "market share acquisition, and inventory liquidation. Corporate sales teams frequently assume that price concessions stimulate sufficient "
        "incremental volume to offset reduced gross margins. However, in the absence of rigorous statistical validation, discounting strategies "
        "frequently degenerate into margin cannibalization, training customers to delay purchases until discounts are granted and systematically "
        "eroding commercial viability."
    )
    add_body_p(doc, 
        "Descriptive analytics and dashboard visualizations often reveal correlations, but correlation alone cannot establish whether observed "
        "differences are statistically distinguishable from random transactional variation. Inferential statistical testing provides the mathematical "
        "framework necessary to test explicit hypotheses, control Type I error rates, calculate population parameter confidence intervals, and quantify "
        "practical effect sizes. This investigation utilizes applied Python inferential tooling to audit retail transactional assumptions and "
        "provide evidence-based recommendations for corporate pricing governance."
    )

    # -------------------------------------------------------------
    # 3. RESEARCH QUESTIONS
    # -------------------------------------------------------------
    add_heading_1(doc, "3. Research Questions")
    add_body_p(doc, "This study formulates and addresses one primary research question and five secondary/exploratory questions:")
    
    rq_items = [
        ("Primary Research Question", "Does receiving a discount significantly affect average order-level profit? Specifically, is there a statistically significant difference in mean net profit between orders receiving a promotional discount (Discount > 0) and orders sold at list price (Discount = 0)?"),
        ("Secondary Question 1", "Does average transactional profit differ significantly across product merchandise categories (Technology, Office Supplies, and Furniture)?"),
        ("Secondary Question 2", "Is there a statistically significant association between order discount status and whether an order yields a net profit or a net operational loss?"),
        ("Secondary Question 3", "How large are the observed statistical differences when quantified using standardized effect sizes (Cohen's d, Eta squared eta^2, and Cramer's V)?"),
        ("Secondary Question 4", "What do the estimated 95% confidence intervals reveal regarding the plausible range of true population differences in transactional profitability?"),
        ("Secondary Question 5", "Are statistically significant empirical differences also meaningful from a practical business and managerial decision-making perspective?")
    ]
    for title, desc in rq_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.2)
        r_bold = p.add_run(f"• {title}: ")
        r_bold.font.name = 'Arial'
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_NAVY
        r_text = p.add_run(desc)
        r_text.font.name = 'Arial'
        r_text.font.color.rgb = COLOR_SLATE

    # -------------------------------------------------------------
    # 4. HYPOTHESIS FORMULATION
    # -------------------------------------------------------------
    add_heading_1(doc, "4. Hypothesis Formulation")
    add_body_p(doc, 
        "To evaluate the research questions objectively, three formal hypothesis testing frameworks are established. "
        "All tests are evaluated against a predefined two-tailed significance threshold of alpha = 0.05."
    )

    add_heading_2(doc, "4.1 Hypothesis 1: Welch's Two-Sample Test on Discount Status")
    add_body_p(doc, "Let mu_discounted represent the population mean profit of discounted orders, and mu_non_discounted represent the population mean profit of undiscounted orders.")
    add_body_p(doc, "• Null Hypothesis (H0): The mean profit of discounted orders is equal to the mean profit of non-discounted orders.\n  H0: mu_discounted = mu_non_discounted")
    add_body_p(doc, "• Alternative Hypothesis (H1): The mean profit of discounted orders differs from the mean profit of non-discounted orders.\n  H1: mu_discounted != mu_non_discounted")

    add_heading_2(doc, "4.2 Hypothesis 2: One-Way ANOVA across Merchandise Categories")
    add_body_p(doc, "Let mu_Furniture, mu_Office_Supplies, and mu_Technology represent the population mean profits for each category.")
    add_body_p(doc, "• Null Hypothesis (H0): All category population mean profits are equal.\n  H0: mu_Furniture = mu_Office_Supplies = mu_Technology")
    add_body_p(doc, "• Alternative Hypothesis (H1): At least one merchandise category has a population mean profit that differs from the others.\n  H1: At least one mu_i != mu_j for i != j")

    add_heading_2(doc, "4.3 Hypothesis 3: Chi-Square Test of Independence on Profitability Status")
    add_body_p(doc, "Let Discount Status be partitioned into {Discounted, No Discount} and Profitability Status into {Profitable, Loss-making}.")
    add_body_p(doc, "• Null Hypothesis (H0): Order discount status and order profitability status are statistically independent.\n  H0: P(Profitability = i, Discount = j) = P(Profitability = i) * P(Discount = j)")
    add_body_p(doc, "• Alternative Hypothesis (H1): Order discount status and order profitability status are statistically dependent (associated).\n  H1: P(Profitability = i, Discount = j) != P(Profitability = i) * P(Discount = j)")

    # -------------------------------------------------------------
    # 5. DATASET OVERVIEW & PREPARATION
    # -------------------------------------------------------------
    add_heading_1(doc, "5. Dataset Overview & Data Preparation")
    add_body_p(doc, 
        "The empirical analysis is conducted on the official Retail Superstore Sales dataset, comprising 9,994 transactional records "
        "spanning four fiscal years. Each record reflects a line-item transaction containing order identifiers, customer segmentation, "
        "geographic metadata, merchandise classification, sales revenue, transaction quantity, promotional discount percentage, and accounting net profit."
    )

    # Data Overview Table
    headers_ds = ["Variable Name", "Data Type", "Role in Study", "Description / Transformation"]
    data_ds = [
        ["Order ID", "String (Categorical)", "Identifier", "Unique alphanumeric transaction code."],
        ["Order / Ship Date", "Datetime", "Temporal Feature", "Parsed to datetime; used to derive Shipping Days."],
        ["Category", "String (Nominal)", "Grouping Factor", "Three levels: Furniture, Office Supplies, Technology."],
        ["Sales", "Float (Continuous)", "Financial Metric", "Gross sales revenue in USD ($0.44 to $22,638.48)."],
        ["Quantity", "Integer (Discrete)", "Operational Metric", "Units purchased per line item (1 to 14)."],
        ["Discount", "Float (Continuous)", "Independent Variable", "Promotional discount rate (0.00 to 0.80)."],
        ["Profit", "Float (Continuous)", "Primary Dependent Variable", "Net profit in USD (-$6,599.98 to +$8,399.98)."],
        ["Discount_Status", "Binary Categorical", "Primary Factor", "'Discounted' (Discount > 0) vs. 'No Discount' (Discount == 0)."],
        ["Profitability_Status", "Binary Categorical", "Contingency Factor", "'Profitable' (Profit > 0) vs. 'Loss-making' (Profit <= 0)."],
        ["Discount_Band", "Ordinal Categorical", "Stratification Factor", "Binned: None (0%), Low (1-10%), Mod (11-20%), High (21-50%), Deep (>50%)."]
    ]
    t_ds = doc.add_table(rows=1, cols=4)
    format_table(t_ds, [Inches(1.5), Inches(1.3), Inches(1.3), Inches(2.4)], headers_ds, data_ds)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Data hygiene protocols verified zero missing values across all target fields. Date columns were standardized, and derived features "
        "were engineered in strict alignment with inferential design requirements. The cleaned analytical table was exported to "
        "data/processed/superstore_cleaned.csv for reproducible execution."
    )

    # -------------------------------------------------------------
    # 6. METHODOLOGY
    # -------------------------------------------------------------
    add_heading_1(doc, "6. Methodology & Statistical Framework")
    add_body_p(doc, 
        "To ensure methodological integrity, testing procedures were selected based on underlying mathematical assumptions, "
        "sample sizes, and variance structures:"
    )
    add_body_p(doc, 
        "1. Significance Level: Set a priori at alpha = 0.05. Test statistics generating p < 0.05 warrant rejection of the null hypothesis. "
        "If p >= 0.05, we state that there is insufficient empirical evidence to reject the null hypothesis; we never claim the null is proven.\n"
        "2. Welch's t-test: Because transaction profit distributions routinely violate homoscedasticity, Student's classic t-test is invalid. "
        "Welch's t-test adjusts degrees of freedom via the Satterthwaite approximation, providing robust Type I error control.\n"
        "3. Mann-Whitney U Sensitivity Check: As profit data exhibits extreme positive and negative outliers, the non-parametric Mann-Whitney U test "
        "evaluates stochastic dominance across ranks, confirming that results are not driven by extreme values.\n"
        "4. One-Way ANOVA & Welch's ANOVA: Standard F-testing evaluates category differences, while Welch's ANOVA is deployed as a robust alternative "
        "when Levene's test reveals unequal group variances. Post-hoc contrasts use Tukey's HSD to control Family-Wise Error Rate (FWER).\n"
        "5. Pearson Chi-Square & Cramer's V: Assesses independence in a 2x2 contingency matrix. Cramer's V standardizes association strength.\n"
        "6. Multiple Testing Control: We apply the Holm-Bonferroni step-down correction across the family of hypothesis tests to prevent FWER inflation."
    )

    # -------------------------------------------------------------
    # 7. DESCRIPTIVE ANALYSIS
    # -------------------------------------------------------------
    add_heading_1(doc, "7. Descriptive & Exploratory Analysis")
    add_body_p(doc, 
        "Descriptive statistics provide foundational insight into the distributional characteristics of the Superstore dataset. "
        "Table 2 outlines univariate properties for key financial measures."
    )

    # Univariate Table
    headers_uni = ["Metric", "Count", "Mean", "Std Dev", "Min", "25%", "Median", "75%", "Max", "Skewness"]
    data_uni = [
        ["Sales ($)", "9,994", "$229.86", "$623.25", "$0.44", "$17.28", "$54.49", "$209.94", "$22,638.48", "+12.97"],
        ["Quantity", "9,994", "3.79", "2.23", "1", "2", "3", "5", "14", "+0.70"],
        ["Discount", "9,994", "0.156", "0.206", "0.000", "0.000", "0.200", "0.200", "0.800", "+1.68"],
        ["Profit ($)", "9,994", "$28.66", "$234.26", "-$6,599.98", "$1.73", "$8.67", "$29.36", "$8,399.98", "+3.44"]
    ]
    t_uni = doc.add_table(rows=1, cols=10)
    format_table(t_uni, [Inches(0.9), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.6), Inches(0.6), Inches(0.6), Inches(0.8), Inches(0.6)], 
                 headers_uni, data_uni, align_rights=[1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Profit demonstrates severe positive skewness (3.44) and extreme kurtosis (397.19), driven by a concentration of modest gains "
        "interspersed with severe catastrophic losses (reaching -$6,600) and substantial windfalls (reaching +$8,400). "
        "The substantial gap between mean profit ($28.66) and median profit ($8.67) highlights the asymmetric influence of tail transactions."
    )

    # Bivariate Breakdown Table
    headers_bi = ["Analytical Subgroup", "Sample Size (N)", "Mean Profit ($)", "Median Profit ($)", "Std Dev ($)", "Loss Rate (%)"]
    data_bi = [
        ["No Discount (Discount == 0)", "4,798 (48.01%)", "$66.90", "$15.995", "$257.06", "0.63% (30 orders)"],
        ["Discounted (Discount > 0)", "5,196 (51.99%)", "-$6.66", "$3.341", "$204.81", "36.68% (1,906 orders)"],
        ["Category: Technology", "1,847 (18.48%)", "$78.75", "$25.018", "$428.82", "14.67%"],
        ["Category: Office Supplies", "6,026 (60.30%)", "$20.33", "$6.882", "$164.89", "14.70%"],
        ["Category: Furniture", "2,121 (21.22%)", "$8.70", "$7.775", "$136.05", "33.66%"],
        ["Discount Band: None (0%)", "4,798", "$66.90", "$15.995", "$257.06", "0.63%"],
        ["Discount Band: Low (1-10%)", "380", "$52.28", "$16.512", "$185.22", "1.32%"],
        ["Discount Band: Mod (11-20%)", "3,657", "$24.12", "$8.286", "$176.81", "13.62%"],
        ["Discount Band: High (21-50%)", "875", "-$124.96", "-$26.310", "$309.28", "88.69%"],
        ["Discount Band: Deep (>50%)", "284", "-$248.91", "-$119.865", "$331.42", "100.00%"]
    ]
    t_bi = doc.add_table(rows=1, cols=6)
    format_table(t_bi, [Inches(2.1), Inches(1.1), Inches(0.9), Inches(0.9), Inches(0.8), Inches(1.0)], headers_bi, data_bi, align_rights=[1, 2, 3, 4, 5])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 8. HYPOTHESIS 1 - WELCH'S T-TEST
    # -------------------------------------------------------------
    add_heading_1(doc, "8. Hypothesis 1 – Independent Two-Sample Welch's t-Test")
    add_body_p(doc, 
        "Primary Question: Do orders receiving promotional discounts yield significantly different average profit than orders sold at list price?"
    )
    add_body_p(doc, 
        "Methodological Justification: Levene's test for equality of variance yielded W = 12.8711 (p = 0.00033). Because the assumption of homoscedasticity "
        "is violated, Student's t-test produces biased standard errors. We deploy Welch's t-test with Satterthwaite degrees of freedom."
    )

    headers_h1 = ["Metric / Parameter", "No Discount Group", "Discounted Group", "Statistical Contrast / Output"]
    data_h1 = [
        ["Sample Size (N)", "4,798 transactions", "5,196 transactions", "Total N = 9,994"],
        ["Sample Mean Profit", "+$66.90 USD", "-$6.66 USD", "Raw Difference = -$73.56 USD"],
        ["Sample Median Profit", "+$15.995 USD", "+$3.341 USD", "Median Difference = -$12.65 USD"],
        ["Sample Standard Deviation", "$257.06 USD", "$204.81 USD", "Variance Ratio = 1.57"],
        ["Welch t-statistic", "--", "--", "t = -15.7380"],
        ["Satterthwaite Degrees of Freedom", "--", "--", "df = 9,162.24"],
        ["Two-Sided p-value", "--", "--", "p = 4.3569e-55 (p < 0.001)"],
        ["95% Confidence Interval of Difference", "--", "--", "[-$82.72 USD, -$64.40 USD]"],
        ["Standardized Effect Size (Cohen's d)", "--", "--", "d = -0.3179 (Hedges' g = -0.3179)"],
        ["Hypothesis Testing Decision", "--", "--", "REJECT NULL HYPOTHESIS (H0)"]
    ]
    t_h1 = doc.add_table(rows=1, cols=4)
    format_table(t_h1, [Inches(1.8), Inches(1.4), Inches(1.4), Inches(1.9)], headers_h1, data_h1)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Technical Interpretation: With t(9162.24) = -15.7380 and p = 4.36e-55, we reject H0. The 95% confidence interval for the mean profit difference "
        "spans [-$82.72, -$64.40]. Because zero is excluded and the entire interval resides in negative territory, we conclude that discounted transactions "
        "earn significantly less than non-discounted transactions. Standardized effect size Cohen's d = -0.3179 denotes a robust, moderate effect."
    )
    add_body_p(doc, 
        "Non-Parametric Robustness Check: The Mann-Whitney U test yielded U = 6,266,805.5, with asymptotic p < 0.0001 and rank-biserial r = 0.4973. "
        "This proves that the observed profit deficit is systemic throughout the distribution and not an artifact of heavy-tailed skewness."
    )

    # -------------------------------------------------------------
    # 9. HYPOTHESIS 2 - ONE-WAY ANOVA
    # -------------------------------------------------------------
    add_heading_1(doc, "9. Hypothesis 2 – One-Way Analysis of Variance (ANOVA)")
    add_body_p(doc, 
        "Secondary Question: Does average order-level profit differ significantly across product categories?"
    )
    add_body_p(doc, 
        "Assumption Auditing: Levene's test across categories produced W = 82.5348 (p = 2.81e-36), demonstrating strong heteroscedasticity. "
        "Technology exhibits substantially higher variance (SD = $428.82) compared to Furniture (SD = $136.05) and Office Supplies (SD = $164.89). "
        "Consequently, both standard Fisher ANOVA and Welch's robust ANOVA are reported."
    )

    headers_h2 = ["Statistical Test", "Test Statistic", "Degrees of Freedom", "p-value", "Effect Size (eta^2)", "Decision"]
    data_h2 = [
        ["Fisher's One-Way ANOVA", "F = 54.3110", "df_between = 2, df_within = 9,991", "3.4699e-24", "eta^2 = 0.0108", "Reject H0"],
        ["Welch's Robust ANOVA", "F_W = 24.0825", "df1 = 2, df2 = 3,587.09", "4.0802e-11", "eta^2 = 0.0108", "Reject H0"]
    ]
    t_h2 = doc.add_table(rows=1, cols=6)
    format_table(t_h2, [Inches(1.6), Inches(1.0), Inches(1.5), Inches(0.9), Inches(0.8), Inches(0.7)], headers_h2, data_h2)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Omnibus Conclusion: Both tests produce p < 0.001, warranting rejection of H0. To identify the exact source of category variation, "
        "we perform post-hoc pairwise contrasts using Tukey's Honestly Significant Difference (HSD) test."
    )

    # Tukey HSD Table
    headers_tukey = ["Comparison (Group 1 vs. Group 2)", "Mean Difference ($)", "Adjusted p-value", "95% CI Lower ($)", "95% CI Upper ($)", "Decision (alpha = 0.05)"]
    data_tukey = [
        ["Furniture vs. Office Supplies", "+$11.63", "0.1181", "-$2.16", "+$25.42", "Fail to Reject (No Diff)"],
        ["Furniture vs. Technology", "+$70.05", "< 0.0001", "+$52.67", "+$87.44", "Reject H0 (Tech Higher)"],
        ["Office Supplies vs. Technology", "+$58.43", "< 0.0001", "+$43.90", "+$72.95", "Reject H0 (Tech Higher)"]
    ]
    t_tukey = doc.add_table(rows=1, cols=6)
    format_table(t_tukey, [Inches(1.8), Inches(1.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.1)], headers_tukey, data_tukey, align_rights=[1, 2, 3, 4])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Post-Hoc Insight: Technology generates significantly higher mean profit than both Furniture ($70.05 higher) and Office Supplies ($58.43 higher). "
        "In contrast, Furniture and Office Supplies show no statistically significant difference (p_adj = 0.1181), demonstrating that category differences "
        "in the Superstore dataset are driven entirely by the premium profitability of Technology merchandise."
    )

    # -------------------------------------------------------------
    # 10. HYPOTHESIS 3 - CHI-SQUARE TEST
    # -------------------------------------------------------------
    add_heading_1(doc, "10. Hypothesis 3 – Pearson's Chi-Square Test of Independence")
    add_body_p(doc, 
        "Secondary Question: Is there a statistically significant association between whether an order receives a discount and whether that order generates a net profit or an operational loss?"
    )

    # 2x2 Contingency Table
    headers_chi = ["Discount Status", "Loss-making (Profit <= 0)", "Profitable (Profit > 0)", "Total Orders", "Observed Loss Rate (%)"]
    data_chi = [
        ["No Discount (Discount == 0)", "30 [Expected: 929.45]", "4,768 [Expected: 3,868.55]", "4,798", "0.63%"],
        ["Discounted (Discount > 0)", "1,906 [Expected: 1,006.55]", "3,290 [Expected: 4,189.45]", "5,196", "36.68%"],
        ["Total Sample", "1,936", "8,058", "9,994", "19.37%"]
    ]
    t_chi = doc.add_table(rows=1, cols=5)
    format_table(t_chi, [Inches(1.8), Inches(1.4), Inches(1.4), Inches(0.9), Inches(1.0)], headers_chi, data_chi, align_rights=[1, 2, 3, 4])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Statistical Results:\n"
        "• Pearson Chi-Square Statistic: Chi2 = 2074.0898\n"
        "• Degrees of Freedom: df = 1\n"
        "• p-value: p < 1e-300 (approaching 0.0000)\n"
        "• Minimum Expected Cell Frequency: 929.45 (far exceeds Cochran's minimum threshold of 5.0)\n"
        "• Effect Size: Cramer's V = 0.4556 (denoting a very strong categorical association)\n"
        "• Odds Ratio (OR): (1,906 * 4,768) / (3,290 * 30) = 91.95"
    )
    add_body_p(doc, 
        "Interpretation: We reject the null hypothesis of independence. The empirical association is astonishingly acute: non-discounted orders "
        "are profitable 99.37% of the time, whereas discounted orders incur losses in 36.68% of transactions. The odds of an order generating a net loss "
        "are nearly 92 times higher when a discount is offered."
    )

    # -------------------------------------------------------------
    # 11. CONFIDENCE INTERVAL ANALYSIS
    # -------------------------------------------------------------
    add_heading_1(doc, "11. Confidence Interval Analysis")
    add_body_p(doc, 
        "A p-value merely indicates whether an effect is distinguishable from zero; it provides no insight into the magnitude or precision of the estimate. "
        "We calculate 95% confidence intervals across key parameters using Student's t distribution with group-specific degrees of freedom."
    )

    headers_ci = ["Estimated Parameter", "Point Estimate", "95% CI Lower", "95% CI Upper", "Methodological Plain-Language Interpretation"]
    data_ci = [
        ["Mean Profit: Technology", "+$78.75", "+$59.20", "+$98.30", "We are 95% confident that the true mean profit for Technology orders lies between $59.20 and $98.30."],
        ["Mean Profit: Office Supplies", "+$20.33", "+$16.16", "+$24.49", "We are 95% confident that the true mean profit for Office Supplies orders lies between $16.16 and $24.49."],
        ["Mean Profit: Furniture", "+$8.70", "+$2.91", "+$14.49", "We are 95% confident that the true mean profit for Furniture orders lies between $2.91 and $14.49."],
        ["Mean Profit: No Discount", "+$66.90", "+$59.63", "+$74.17", "We are 95% confident that undiscounted transactions yield an expected profit between $59.63 and $74.17."],
        ["Mean Profit: Discounted", "-$6.66", "-$12.22", "-$1.09", "We are 95% confident that discounted transactions yield an expected profit between -$12.22 and -$1.09."],
        ["Mean Difference (Disc - No Disc)", "-$73.56", "-$82.72", "-$64.40", "We are 95% confident that discounting reduces expected order profit by between $64.40 and $82.72."]
    ]
    t_ci = doc.add_table(rows=1, cols=5)
    format_table(t_ci, [Inches(1.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(2.3)], headers_ci, data_ci, align_rights=[1, 2, 3])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Rigorous Confidence Interval Interpretation: In frequentist statistics, a 95% confidence interval does NOT mean there is a 95% probability "
        "that the fixed population parameter falls within this specific numerical window. Rather, it means that if the identical sampling and estimation "
        "procedure were repeated across 100 independent random samples from the same population, 95 of the constructed confidence intervals would successfully "
        "contain the true, fixed population parameter."
    )

    # -------------------------------------------------------------
    # 12. CONSOLIDATED STATISTICAL RESULTS
    # -------------------------------------------------------------
    add_heading_1(doc, "12. Consolidated Statistical Results Table")
    add_body_p(doc, 
        "Table 7 integrates all empirical statistical tests conducted in this study, recording the exact test statistics, degrees of freedom, "
        "p-values, standardized effect sizes, confidence intervals, formal testing decisions, and analytical interpretations."
    )

    headers_con = ["Test Executed", "Research Question", "Statistic & df", "p-value", "Effect Size", "95% CI", "Decision"]
    data_con = [
        ["Welch t-test (Primary)", "Does discount affect mean profit?", "t = -15.7380\ndf = 9162.24", "4.3569e-55", "Cohen's d = -0.3179", "[-$82.72, -$64.40]", "Reject H0"],
        ["Mann-Whitney U (Sensitivity)", "Is profit rank distribution shifted?", "U = 6,266,805.5\nRank Sum", "< 0.0001", "Rank-biserial r = 0.4973", "N/A", "Reject H0"],
        ["One-Way ANOVA (Secondary)", "Does profit differ by category?", "F = 54.3110\ndf = (2, 9991)", "3.4699e-24", "Eta^2 = 0.0108", "Category specific", "Reject H0"],
        ["Welch's ANOVA (Robust)", "Category profit under unequal var?", "F_W = 24.0825\ndf = (2, 3587)", "4.0802e-11", "Eta^2 = 0.0108", "Category specific", "Reject H0"],
        ["Chi-Square Test (Secondary)", "Is discount associated with loss?", "Chi2 = 2074.0898\ndf = 1", "< 1e-300", "Cramer's V = 0.4556", "OR = 91.95", "Reject H0"]
    ]
    t_con = doc.add_table(rows=1, cols=7)
    format_table(t_con, [Inches(1.4), Inches(1.3), Inches(1.0), Inches(0.7), Inches(0.9), Inches(0.8), Inches(0.6)], headers_con, data_con)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Multiple testing paragraph
    add_body_p(doc, 
        "Multiple Testing Control (Holm-Bonferroni Method): Evaluating multiple statistical hypotheses simultaneously inflates the Family-Wise "
        "Error Rate (FWER). To safeguard against spurious discoveries, the Holm-Bonferroni step-down correction was applied across the family of tests. "
        "Because all raw p-values are orders of magnitude below their respective adjusted alpha thresholds (e.g., Welch t-test p = 4.36e-55 vs. threshold 0.0100; "
        "Chi-square p < 1e-300 vs. threshold 0.0125), all primary and secondary findings maintain statistical significance."
    )

    # -------------------------------------------------------------
    # 13. VISUAL ANALYSIS
    # -------------------------------------------------------------
    add_heading_1(doc, "13. Visual Analysis & Statistical Interpretation")
    add_body_p(doc, 
        "Statistical visualizations are critical for communicating empirical findings to executive stakeholders. "
        "Below, each of the seven publication-standard visualizations generated by our analytical pipeline is presented with its complete "
        "five-part analytical evaluation: (1) Research Question Addressed, (2) Selection Rationale, (3) Empirical Observation, "
        "(4) Statistical Interpretation, and (5) Strategic Business Implication."
    )

    viz_details = [
        {
            "num": "1",
            "file": "01_profit_distribution.png",
            "title": "Figure 1: Superstore Transaction Profit Distribution & Skewness Analysis",
            "q": "What is the overall distributional shape, central tendency, and dispersion of order-level profit?",
            "why": "A dual-panel design combining a logarithmic histogram for extreme tail exposure with a focused central histogram ([-$250, +$250]) ensures full visibility of both extreme outliers and the bulk density.",
            "obs": "Profit displays positive skewness (+3.44) and extreme kurtosis (+397.19). While 80.6% of orders generate profit, severe left-tail losses plunge to -$6,600, while right-tail gains reach +$8,400.",
            "stat": "The divergence between mean profit ($28.66) and median profit ($8.67) indicates heavy right-tail pull, while the extreme standard deviation ($234.26) confirms high transactional volatility. Parametric CLT validity relies on large sample size (N = 9,994).",
            "biz": "Corporate averages are misleading. Management must focus on loss prevention in the catastrophic left tail rather than celebrating nominal revenue spikes that conceal devastating margin destruction."
        },
        {
            "num": "2",
            "file": "02_discount_vs_profit.png",
            "title": "Figure 2: Transaction Discount Rate vs. Net Profit (Scatter Plot & Regression Trend)",
            "q": "What is the empirical functional relationship between promotional discount rates and net profit?",
            "why": "A scatter plot with alpha transparency and discrete jitter resolves data point overlap while overlaying an OLS regression trend line to visualize directional slope across discount increments.",
            "obs": "Profit remains reliably positive for discounts of 0% to 15%. However, beyond the 20% discount threshold, transactions experience severe downward variance, with discounts of 40% to 80% generating catastrophic losses.",
            "stat": "The negative regression slope confirms strong inverse correlation (r = -0.22, p < 0.001). However, correlation does NOT establish causality: product selection, regional pricing, and transaction size may confound the relationship.",
            "biz": "A non-linear 'tipping point' exists at 20% discount. Commercial leadership should establish a strict policy prohibition against unapproved discounts exceeding 20%."
        },
        {
            "num": "3",
            "file": "03_group_comparison.png",
            "title": "Figure 3: Profit Comparison: No Discount (N=4,798) vs. Discounted (N=5,196)",
            "q": "How do profit distributions compare between discounted and non-discounted transactions?",
            "why": "Side-by-side truncated box plots and violin density plots provide simultaneous clarity on median quartiles, diamond mean markers, and density multimodal profiles.",
            "obs": "Non-discounted orders exhibit a tight, positive interquartile range (IQR = $30.82, median = $15.99, mean = $66.90). Discounted orders show a negative mean (-$6.66), lower median ($3.34), and heavy downward density.",
            "stat": "Welch's t-test verifies that the mean shift (-$73.56) is highly significant (t = -15.7380, p = 4.36e-55). Levene's test confirms significant variance inequality (p = 0.00033).",
            "biz": "Discounting fails to generate profitable operational scale. Non-discounted transactions represent the core financial engine of the enterprise."
        },
        {
            "num": "4",
            "file": "04_category_profit_distribution.png",
            "title": "Figure 4: Profit Distribution Across Product Categories (Excl. Outliers)",
            "q": "How does profitability vary across the three merchandise categories (Technology, Office Supplies, Furniture)?",
            "why": "Standardized category box plots with embedded numeric badges allow direct visual benchmarking of category medians, means, and spread.",
            "obs": "Technology demonstrates superior mean profitability ($78.75) and higher median ($25.02). Office Supplies exhibits moderate performance (mean $20.33, median $6.88). Furniture exhibits the weakest mean ($8.70, median $7.77).",
            "stat": "One-Way ANOVA confirms significant omnibus category variance (F = 54.31, p = 3.47e-24). Variance heterogeneity is severe (Technology SD = $428.82 vs. Furniture SD = $136.05).",
            "biz": "Technology can absorb selective promotional discounting due to high gross margins. Furniture cannot tolerate aggressive discounts without suffering operational deficits."
        },
        {
            "num": "5",
            "file": "05_anova_comparison.png",
            "title": "Figure 5: One-Way ANOVA: Mean Category Profit with 95% Confidence Intervals",
            "q": "Which product category pairs exhibit statistically significant differences in mean profit?",
            "why": "A clear bar chart with 95% confidence interval error bars, exact sample size labels, and Tukey HSD significance brackets clearly communicates inferential conclusions to non-technical leaders.",
            "obs": "Technology's confidence interval [$59.20, $98.30] is entirely disjoint from Office Supplies [$16.16, $24.49] and Furniture [$2.91, $14.49]. Furniture and Office Supplies overlap substantially.",
            "stat": "Tukey HSD confirms Technology differs significantly from Furniture (diff = $70.05, p < 0.001) and Office Supplies (diff = $58.43, p < 0.001). Furniture vs. Office Supplies is not significant (diff = $11.63, p = 0.1181).",
            "biz": "Strategic investment and marketing focus should prioritize Technology. Furniture requires operational restructuring rather than discounting incentives."
        },
        {
            "num": "6",
            "file": "06_contingency_heatmap.png",
            "title": "Figure 6: Discount Status × Profitability Association Heatmap",
            "q": "What is the structural association between discount status and order profitability status?",
            "why": "Dual heatmaps presenting absolute transaction counts alongside within-group row percentages provide both statistical rigor and immediate commercial clarity.",
            "obs": "Undiscounted orders yield an exceptional 99.37% profit rate (only 30 losses in 4,798 orders). Discounted orders suffer a 36.68% loss rate (1,906 losses in 5,196 orders).",
            "stat": "Pearson Chi-Square test confirms massive dependence (Chi2 = 2074.0898, p < 1e-300, df = 1). Cramer's V = 0.4556 indicates strong categorical effect size. Odds Ratio = 91.95.",
            "biz": "Discounting converts a near-certain profit (99.4%) into a more than 1-in-3 chance of an operational loss. Sales reps offering discounts are directly generating balance sheet deficits."
        },
        {
            "num": "7",
            "file": "07_confidence_intervals.png",
            "title": "Figure 7: Summary of Estimated 95% Confidence Intervals (Forest Plot)",
            "q": "What are the precision boundaries for category means, group means, and the overall difference estimate?",
            "why": "A standardized two-panel forest plot displays parameter point estimates and margin-of-error whiskers against a vertical zero-effect baseline.",
            "obs": "The mean difference interval [-$82.72, -$64.40] is cleanly isolated from zero. Category intervals demonstrate high estimation precision due to substantial sample sizes.",
            "stat": "Because the 95% CI for the mean difference does not contain zero, the null hypothesis H0: mu_disc = mu_nodisc is decisively rejected at alpha = 0.05.",
            "biz": "Executive planning can rely on these boundaries: even under the most conservative interpretation of sampling error, discounting costs the enterprise at least $64.40 per transaction."
        }
    ]

    for it in viz_details:
        add_heading_2(doc, it["title"])
        img_path = os.path.join(viz_dir, it["file"])
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(6.0))
        
        # 5-Part Analytical Breakdown
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        p_cap.paragraph_format.left_indent = Inches(0.15)
        
        breakdown_text = [
            ("Research Question Addressed: ", it["q"]),
            ("Chart Selection Rationale: ", it["why"]),
            ("Empirical Observations: ", it["obs"]),
            ("Statistical Interpretation: ", it["stat"]),
            ("Strategic Business Implications: ", it["biz"])
        ]
        for lbl, val in breakdown_text:
            p_item = doc.add_paragraph()
            p_item.paragraph_format.space_before = Pt(1)
            p_item.paragraph_format.space_after = Pt(2)
            p_item.paragraph_format.left_indent = Inches(0.2)
            r_b = p_item.add_run(lbl)
            r_b.font.name = 'Arial'
            r_b.font.size = Pt(9.5)
            r_b.font.bold = True
            r_b.font.color.rgb = COLOR_NAVY
            r_v = p_item.add_run(val)
            r_v.font.name = 'Arial'
            r_v.font.size = Pt(9.5)
            r_v.font.color.rgb = COLOR_SLATE
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 14. OVERALL FINDINGS
    # -------------------------------------------------------------
    add_heading_1(doc, "14. Overall Findings Synthesis")
    add_body_p(doc, 
        "Integrating the empirical results of our three hypothesis testing frameworks reveals a coherent, data-driven narrative "
        "regarding Superstore commercial dynamics:"
    )
    add_body_p(doc, 
        "1. Primary Discount Drag: Promotional discounting is associated with a statistically significant, commercially crippling reduction in mean profit (-$73.56 per order, t = -15.7380, p < 0.001). Cohen's d of -0.3179 confirms a robust practical effect.\n"
        "2. Skewness Robustness: Distributional skewness and extreme outliers do not explain away this finding; the Mann-Whitney U test confirms that the median profit ranking is severely degraded by discounting (U = 6,266,805.5, p < 0.0001, rank-biserial r = 0.4973).\n"
        "3. Structural Category Hierarchy: Technology is the premier profit driver ($78.75 mean profit), significantly exceeding Furniture ($8.70) and Office Supplies ($20.33) in One-Way ANOVA (F = 54.31, p < 0.001) and post-hoc Tukey HSD tests. Furniture and Office Supplies perform similarly.\n"
        "4. Acute Loss Escalation: Discounting creates an acute surge in operational losses (Chi2 = 2074.09, p < 1e-300, Cramer's V = 0.4556). Non-discounted transactions achieve a 99.37% profit rate, while discounted transactions fail in 36.68% of cases (Odds Ratio = 91.95).\n"
        "5. Family-Wise Error Robustness: All statistical conclusions survive Holm-Bonferroni step-down correction with adjusted p-values far below 0.001."
    )

    # -------------------------------------------------------------
    # 15. BUSINESS IMPLICATIONS
    # -------------------------------------------------------------
    add_heading_1(doc, "15. Business Implications & Strategic Recommendations")
    add_body_p(doc, 
        "The empirical findings carry direct, actionable implications for corporate pricing strategy, commercial compensation, "
        "and inventory management:"
    )
    add_body_p(doc, 
        "1. Eliminate Blanket Discounting: Broad, discretionary price cuts must be abolished immediately. Across 5,196 discounted orders, the company incurred a cumulative profit deficit relative to list-price sales.\n"
        "2. Enforce a 20% Hard Discount Ceiling: Data reveals a clear non-linear cliff at 20% discount. Discounts between 1% and 20% maintain positive average profits, but discounts exceeding 20% produce an 88.7% loss rate. Any discount > 20% should require executive approval.\n"
        "3. Protect Fragile Furniture Margins: Furniture exhibits a meager mean profit of $8.70 and an overall loss rate of 33.66%. The company cannot afford promotional discounts on Furniture without restructuring supplier acquisition costs.\n"
        "4. Align Sales Incentives with Net Profit: If sales compensation is tied strictly to top-line gross revenue, sales reps are economically incentivized to grant 40-70% discounts to close volume, transferring all financial loss to the enterprise. Compensation must be indexed to gross margin contribution."
    )

    # -------------------------------------------------------------
    # 16. LIMITATIONS
    # -------------------------------------------------------------
    add_heading_1(doc, "16. Methodological Limitations")
    add_body_p(doc, 
        "Scientific rigor requires transparent acknowledgement of study limitations:\n"
        "1. Observational Design (Association vs. Causation): Transactions were not assigned discounts via a randomized controlled trial (A/B experiment). Consequently, discounting is correlated with lower profit, but we cannot assert definitive causal directionality without controlling for unobserved commercial factors.\n"
        "2. Unobserved Confounders: The dataset lacks critical variables such as product cost-of-goods-sold (COGS) inflation, supplier volume rebates, shipping freight contracts, and regional sales quotas.\n"
        "3. Customer Lifetime Value (CLV) Absence: The dataset records isolated order-level accounting profit. It does not measure customer retention, repeat purchase velocity, or acquisition economics. A loss-making first order might theoretically be economically rational if it secures a highly profitable long-term corporate account.\n"
        "4. Extreme Outlier Leverage: While the Mann-Whitney U test confirmed rank-based robustness, parametric mean estimates remain sensitive to extreme single-order swings (e.g., -$6,600 losses)."
    )

    # -------------------------------------------------------------
    # 17. FUTURE WORK
    # -------------------------------------------------------------
    add_heading_1(doc, "17. Future Research & Analytical Scope")
    add_body_p(doc, 
        "To build upon this foundational statistical study, subsequent analytical phases should implement:\n"
        "1. Econometric Causal Modeling: Deploy Propensity Score Matching (PSM) and Instrumental Variable (IV) estimation to isolate true causal price elasticity.\n"
        "2. Randomized Controlled Experiments: Design structured A/B tests across regional marketing channels with randomized discount tiers to establish experimental causality.\n"
        "3. Multivariate Regression & Machine Learning: Fit regularized regression (Lasso/Ridge) and Gradient Boosting trees (XGBoost) to predict profit elasticity across sub-categories and customer segments.\n"
        "4. Customer Cohort LTV Modeling: Aggregate transactional logs to customer-level profiles to model long-term retention dynamics."
    )

    # -------------------------------------------------------------
    # 18. CONCLUSION
    # -------------------------------------------------------------
    add_heading_1(doc, "18. Final Conclusion")
    add_body_p(doc, 
        "This project successfully answers all primary and secondary research questions established for the YUVA Week 3 internship task:\n\n"
        "1. What did the primary hypothesis test show?\n"
        "The primary Welch's t-test demonstrated that orders receiving promotional discounts have a statistically significant, negative mean profit (-$6.66) "
        "compared to non-discounted orders (+$66.90), representing an observed deficit of -$73.56 per order (t = -15.7380, df = 9162.24, p = 4.36e-55).\n\n"
        "2. What did the ANOVA show?\n"
        "The One-Way ANOVA established significant profit differences across merchandise categories (F = 54.3110, p = 3.47e-24, eta^2 = 0.0108), confirmed via Welch's robust ANOVA (F_W = 24.0825, p = 4.08e-11). Post-hoc Tukey HSD proved this variation is driven by Technology ($78.75), while Furniture ($8.70) and Office Supplies ($20.33) do not significantly differ.\n\n"
        "3. What did the chi-square test show?\n"
        "The Chi-Square test revealed a massive statistical association between discount status and profitability status (Chi2 = 2074.0898, df = 1, p < 1e-300, Cramer's V = 0.4556). Non-discounted orders exhibit a 99.37% profit rate, while discounted orders incur losses in 36.68% of cases (Odds Ratio = 91.95).\n\n"
        "4. Which hypotheses were rejected or not rejected?\n"
        "Hypothesis 1 (Welch t-test) was REJECTED. Hypothesis 2 (ANOVA) was REJECTED. Hypothesis 3 (Chi-Square) was REJECTED. In post-hoc analysis, Furniture vs. Technology and Office Supplies vs. Technology were REJECTED, while Furniture vs. Office Supplies FAILED TO REJECT.\n\n"
        "5. Were the effects practically meaningful?\n"
        "Yes. Standardized effect sizes (Cohen's d = -0.3179, Cramer's V = 0.4556, Odds Ratio = 91.95) confirm that findings represent substantial commercial margin erosion rather than trivial statistical artifacts.\n\n"
        "6. What are the business implications?\n"
        "Retail leadership must establish a 20% hard discount ceiling, abolish discretionary sales rep discounting, protect fragile Furniture margins, and index sales incentives to gross profit contribution.\n\n"
        "7. What should be investigated next?\n"
        "Management should initiate randomized A/B discount elasticity trials, implement multivariate regularized regression models, and conduct customer-level lifetime value (CLV) cohort tracking."
    )

    # -------------------------------------------------------------
    # 19. REFERENCES
    # -------------------------------------------------------------
    add_heading_1(doc, "19. References & Methodological Sources")
    refs = [
        "1. Superstore Sales Dataset. Publicly accessible corporate retail transactional dataset (9,994 records).",
        "2. McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51-56.",
        "3. Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17(3), 261-272.",
        "4. Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and Statistical Modeling with Python. Proceedings of the 9th Python in Science Conference.",
        "5. Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), 90-95.",
        "6. Waskom, M. L. (2021). Seaborn: Statistical Data Visualization. Journal of Open Source Software, 6(60), 3021.",
        "7. Welch, B. L. (1947). The generalization of 'Student's' problem when several different population variances are involved. Biometrika, 34(1/2), 28-35.",
        "8. Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics, 6(2), 65-70."
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.2)
        r_run = p.add_run(r)
        r_run.font.name = 'Arial'
        r_run.font.size = Pt(9)
        r_run.font.color.rgb = COLOR_SLATE

    # -------------------------------------------------------------
    # 20. CODE SNIPPETS
    # -------------------------------------------------------------
    add_heading_1(doc, "20. Reproducible Python Code Snippets")
    add_body_p(doc, 
        "Below are the core Python code snippets demonstrating the implementation of data preparation, hypothesis testing, "
        "and confidence interval estimation in our reproducible codebase:"
    )

    snippets = [
        ("Snippet 1: Data Ingestion & Encoding Handling (src/data_loading.py)", """
import pandas as pd

def load_raw_data(filepath):
    for enc in ['windows-1252', 'utf-8', 'latin1']:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("Failed to load dataset across supported encodings.")
"""),
        ("Snippet 2: Feature Engineering & Preprocessing (src/preprocessing.py)", """
import numpy as np

# Construct binary discount and profitability indicators
df['Discount_Status'] = np.where(df['Discount'] > 0, 'Discounted', 'No Discount')
df['Profitability_Status'] = np.where(df['Profit'] > 0, 'Profitable', 'Loss-making')
df['Profit_Margin'] = np.where(df['Sales'] > 0, df['Profit'] / df['Sales'], 0.0)
"""),
        ("Snippet 3: Welch's Two-Sample t-Test & Effect Size (src/hypothesis_tests.py)", """
from scipy import stats
import numpy as np

disc = df[df['Discount_Status'] == 'Discounted']['Profit']
nodisc = df[df['Discount_Status'] == 'No Discount']['Profit']

# Two-sided Welch t-test (equal_var=False)
t_stat, p_val = stats.ttest_ind(disc, nodisc, equal_var=False)

# Pooled standard deviation & Cohen's d
n1, n2 = len(disc), len(nodisc)
s_pooled = np.sqrt(((n1 - 1)*disc.var() + (n2 - 1)*nodisc.var()) / (n1 + n2 - 2))
cohens_d = (disc.mean() - nodisc.mean()) / s_pooled
"""),
        ("Snippet 4: One-Way ANOVA & Tukey HSD Post-Hoc Analysis", """
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# One-Way ANOVA across categories
cat_groups = [df[df['Category'] == c]['Profit'] for c in df['Category'].unique()]
f_stat, anova_p = stats.f_oneway(*cat_groups)

# Tukey HSD pairwise post-hoc test
tukey = pairwise_tukeyhsd(endog=df['Profit'], groups=df['Category'], alpha=0.05)
print(tukey)
"""),
        ("Snippet 5: Pearson's Chi-Square Test & Cramer's V", """
import pandas as pd
from scipy import stats
import numpy as np

# Contingency table
ct = pd.crosstab(df['Discount_Status'], df['Profitability_Status'])
chi2, p_val, dof, expected = stats.chi2_contingency(ct)

# Cramer's V calculation
n = ct.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
"""),
        ("Snippet 6: 95% Confidence Interval Calculation", """
from scipy import stats

def compute_95_ci(series):
    mean_val = series.mean()
    sem_val = stats.sem(series)
    return stats.t.interval(0.95, df=len(series)-1, loc=mean_val, scale=sem_val)
""")
    ]

    for title, code_block in snippets:
        add_heading_2(doc, title)
        add_code_block(doc, code_block)

    # Save document
    os.makedirs(os.path.dirname(output_docx_path), exist_ok=True)
    doc.save(output_docx_path)
    print(f"[SUCCESS] High-quality DOCX report successfully generated at: {output_docx_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_docx = os.path.join(base_dir, "yuva-week3-statistical-analysis", "report", "YUVA_Week3_Statistical_Analysis_Report.docx")
    viz_directory = os.path.join(base_dir, "yuva-week3-statistical-analysis", "visualizations")
    build_docx_report(out_docx, viz_directory)
