# Data Dictionary

## Project

**Banking Customer Churn Analysis**  
This data dictionary documents the cleaned customer churn dataset used for exploratory analysis, statistical testing, KPI calculation, and Tableau dashboarding.

## Dataset Summary

| Item | Description |
|---|---|
| Clean dataset | `data/churn_clean.csv` |
| Raw dataset | `data/churn_prediction.csv` |
| Number of records | 28,382 customers |
| Number of cleaned columns | 26 |
| Target variable | `churn` |
| Churn coding | `1 = Churned`, `0 = Retained` |
| Overall churn rate | 18.53% |
| Main analysis goal | Identify customer groups with higher churn risk and prepare KPI-ready data for Tableau |

## Column Definitions

| Column | Type | Description | Example / Values |
|---|---|---|---|
| `vintage` | Integer | Customer relationship duration with the bank, usually measured in months. Used to understand loyalty and tenure. | `24`, `60`, `120` |
| `age` | Integer | Customer age in years. Used for customer segmentation and churn pattern analysis. | `25`, `42`, `67` |
| `gender` | Categorical | Customer gender after cleaning missing/invalid values. | `Male`, `Female` |
| `dependents` | Float | Number of dependents linked to the customer. Missing values are filled with the median. | `0`, `1`, `2` |
| `occupation` | Categorical | Customer occupation group. Missing occupations are labelled as `Unknown`. | `self_employed`, `salaried`, `student`, `retired`, `company`, `Unknown` |
| `customer_nw_category` | Integer | Customer net worth category assigned by the bank. Lower or higher categories may indicate different financial profiles. | `1`, `2`, `3` |
| `current_balance` | Float | Current account balance after negative-value handling and outlier capping. | `1520.75` |
| `previous_month_end_balance` | Float | Balance at the end of the previous month. Used to compare balance movement. | `2480.00` |
| `average_monthly_balance_prevQ` | Float | Average monthly balance in the previous quarter. | `3100.50` |
| `average_monthly_balance_prevQ2` | Float | Average monthly balance in the quarter before the previous quarter. | `2950.25` |
| `current_month_credit` | Float | Total credited amount in the current month after cleaning. | `5000.00` |
| `previous_month_credit` | Float | Total credited amount in the previous month after cleaning. | `4200.00` |
| `current_month_debit` | Float | Total debited amount in the current month after cleaning. | `3500.00` |
| `previous_month_debit` | Float | Total debited amount in the previous month after cleaning. | `2800.00` |
| `current_month_balance` | Float | Average or derived balance measure for the current month. | `2700.00` |
| `previous_month_balance` | Float | Average or derived balance measure for the previous month. | `2600.00` |
| `churn` | Integer | Target variable showing whether the customer churned. | `1 = Churned`, `0 = Retained` |
| `last_transaction` | Date | Date of the customer's last transaction. Missing values indicate no recorded recent transaction. | `2019-08-21` |
| `transaction_year` | Float | Year extracted from `last_transaction`. Missing when `last_transaction` is missing. | `2019` |
| `transaction_month` | Float | Month extracted from `last_transaction`. Missing when `last_transaction` is missing. | `8` |
| `transaction_day` | Float | Day extracted from `last_transaction`. Missing when `last_transaction` is missing. | `21` |
| `no_transaction_flag` | Integer | Flag created to identify customers with no recorded transaction date. | `1 = No transaction date`, `0 = Transaction date available` |
| `age_group` | Categorical | Age segment created for business-friendly analysis. | `Young`, `Adult`, `Middle Age`, `Senior` |
| `balance_segment` | Categorical | Balance segment based on `current_balance`. | `Low`, `Medium`, `High` |
| `total_transactions` | Float | Derived feature calculated as `current_month_credit + current_month_debit`. | `8500.00` |
| `activity_level` | Categorical | Customer activity segment based on `total_transactions`. | `Low Activity`, `Moderate`, `High`, `Very High` |

## Derived Feature Logic

| Feature | Logic |
|---|---|
| `age_group` | `Young: 0-25`, `Adult: 26-40`, `Middle Age: 41-60`, `Senior: 61+` |
| `balance_segment` | `Low: <= 1,000`, `Medium: 1,001-10,000`, `High: > 10,000` |
| `total_transactions` | `current_month_credit + current_month_debit` |
| `activity_level` | `Low Activity: <= 1,000`, `Moderate: 1,001-10,000`, `High: 10,001-50,000`, `Very High: > 50,000` |
| `no_transaction_flag` | `1` when `last_transaction` is missing, otherwise `0` |

## Cleaning Rules Applied

1. Removed duplicate rows.
2. Dropped non-analytical identifiers: `customer_id`, `branch_code`, and `city`.
3. Filled missing `gender` with the most frequent gender.
4. Replaced `Other` in `gender` with the most frequent gender to keep gender analysis consistent.
5. Filled missing `dependents` with the median.
6. Filled missing `occupation` with `Unknown`.
7. Replaced negative monetary values with `0`.
8. Capped monetary outliers using the 1st and 99th percentiles.
9. Converted `last_transaction` to date format.
10. Created transaction date features and business segments for EDA, KPI reporting, and Tableau.

## Tableau Export Files

The final notebook creates Tableau-ready CSV files in `data/tableau_exports/`:

| File | Purpose |
|---|---|
| `kpi_summary.csv` | Overall churn KPI summary |
| `churn_by_age_group.csv` | Churn rate by age segment |
| `churn_by_gender.csv` | Churn rate by gender |
| `churn_by_occupation.csv` | Churn rate by occupation |
| `churn_by_balance_segment.csv` | Churn rate by balance segment |
| `churn_by_activity_level.csv` | Churn rate by activity level |
| `churn_by_vintage_bucket.csv` | Churn rate by customer tenure bucket |
| `churn_final_tableau.csv` | Full master dataset for Tableau dashboards |

## Known Limitations

- The dataset does not include direct customer feedback, complaint history, digital banking usage, or product ownership details.
- Churn is treated as a binary outcome, so the analysis explains churn patterns but does not predict future churn probabilities.
- Some transaction-date fields remain missing by design and are tracked using `no_transaction_flag`.
- Outlier treatment improves analysis stability but may reduce the visibility of rare extreme-value customers.

