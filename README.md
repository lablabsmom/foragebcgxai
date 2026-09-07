# SEC 10-K Financial Analysis

A small pandas-based analysis of key financial metrics for Microsoft, Tesla, and
Apple, extracted manually from their 10-K filings on SEC EDGAR for fiscal years
2023–2025.

## What it does

- Loads normalized filing data (Revenue, Net Income, Total Assets, Total
  Liabilities, Operating Cash Flow) from a CSV.
- Calculates year-over-year percentage change for Revenue, Net Income, and
  Operating Cash Flow.
- Derives financial health indicators: Net Margin, Operating Cash Flow Margin,
  and Liabilities-to-Assets ratio.
- Summarizes the overall (first-year to last-year) percentage change per
  company across all core metrics.

## Project structure

```
sec-10k-analysis/
├── analyze_filings.py                 # CLI script version
├── analyze_filings.ipynb              # notebook version with narrative
├── data/
│   ├── financial_data.csv             # manually extracted input data
│   └── financial_analysis_results.csv # generated output (optional to commit)
├── README.md
└── .gitignore
```

## Data source

Figures were extracted manually from each company's 10-K filings on
[SEC EDGAR](https://www.sec.gov/edgar/search/):

- [Microsoft](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K)
- [Tesla](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-K)
- [Apple](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K)

`data/financial_data.csv` must contain the columns: `Company`, `Year`,
`Revenue`, `Net Income`, `Total Assets`, `Total Liabilities`,
`Operating Cash Flow`.

## Usage

Install dependencies:

```bash
pip install pandas
```

Run the script:

```bash
python analyze_filings.py --input data/financial_data.csv --output data/financial_analysis_results.csv
```

Or open `analyze_filings.ipynb` in Jupyter / VS Code / Colab / GitHub
Codespaces to walk through the same analysis with narrative explanations.

## Disclaimer

This project was built as part of a BCG GenAI Consulting simulation exercise
(via Forage) and is for educational purposes only.
