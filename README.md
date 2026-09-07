# foragebcgxai
Built as the data-extraction-and-analysis phase of a larger GenAI consulting project: turning raw 10-K financial statements into clean, structured, AI-ready data. (for FORAGE BCGx AI)
# SEC 10-K Financial Analysis

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![pandas](https://img.shields.io/badge/pandas-data%20analysis-150458)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-educational%20project-lightgrey)

A pandas-based financial analysis pipeline that extracts insights from
10-K filings for **Microsoft, Tesla, and Apple** (fiscal years 2023–2025).
It calculates year-over-year growth, profitability, and leverage metrics,
and lays the groundwork for feeding structured financial data into an
AI-powered financial chatbot.

Built as the data-extraction-and-analysis phase of a larger GenAI
consulting project: turning raw 10-K financial statements into clean,
structured, AI-ready data.

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Project structure](#project-structure)
- [Data source](#data-source)
- [Data schema](#data-schema)
- [Installation](#installation)
- [Usage](#usage)
  - [Script](#run-as-a-script)
  - [Notebook](#run-as-a-notebook)
- [Metrics explained](#metrics-explained)
- [Sample output](#sample-output)
- [Methodology notes](#methodology-notes)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Overview

Traditional financial analysis of 10-K and 10-Q filings is slow and
manual. This project is a first step toward automating that process: it
takes manually extracted, normalized filing data and runs a repeatable
pandas pipeline over it to surface trends, growth rates, and financial
health indicators — the kind of structured insight an AI chatbot could
later use to answer natural-language questions like *"How did Apple's
margin change between 2023 and 2025?"*

## Features

- **Data validation** — checks that all required columns are present
  before any analysis runs.
- **Year-over-year growth** — Revenue, Net Income, and Operating Cash
  Flow, calculated per company so growth is never blended across
  companies.
- **Financial health indicators**:
  - Net Margin (%)
  - Operating Cash Flow Margin (%)
  - Liabilities-to-Assets (%)
- **Multi-year summary** — first-year-to-last-year percentage change for
  every core metric, per company, for a quick "big picture" view.
- **Two ways to run it** — a CLI script (`analyze_filings.py`) for
  automation/pipelines, and a Jupyter notebook
  (`analyze_filings.ipynb`) with narrative markdown for exploratory,
  documented analysis.
- **CSV in, CSV out** — results are exported to a clean CSV, ready to
  hand off to downstream tools (e.g. a chatbot's retrieval layer).

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

| Company   | EDGAR filing history |
|-----------|-----------------------|
| Microsoft | [10-K filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K) |
| Tesla     | [10-K filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-K) |
| Apple     | [10-K filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K) |

For each company and year, five figures were pulled from the Income
Statement, Balance Sheet, and Cash Flow Statement sections of the 10-K:
**Total Revenue, Net Income, Total Assets, Total Liabilities,** and
**Cash Flow from Operating Activities**.

## Data schema

`data/financial_data.csv` must contain the following columns. All
financial figures should be normalized to the same unit (e.g. millions
of USD) before loading.

| Column               | Type   | Description                                   |
|-----------------------|--------|------------------------------------------------|
| `Company`             | string | Company name (e.g. `Microsoft`, `Tesla`, `Apple`) |
| `Year`                | int    | Fiscal year (e.g. `2023`, `2024`, `2025`)      |
| `Revenue`              | float  | Total revenue for the fiscal year              |
| `Net Income`           | float  | Net income for the fiscal year                 |
| `Total Assets`         | float  | Total assets at fiscal year end                |
| `Total Liabilities`    | float  | Total liabilities at fiscal year end           |
| `Operating Cash Flow`  | float  | Cash flow from operating activities            |

Example row:

```csv
Company,Year,Revenue,Net Income,Total Assets,Total Liabilities,Operating Cash Flow
Microsoft,2023,211915,72361,411976,205753,87582
```

## Installation

Requires **Python 3.9+**.

```bash
git clone https://github.com/YOUR-USERNAME/sec-10k-analysis.git
cd sec-10k-analysis
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, this project only needs:

```bash
pip install pandas matplotlib notebook
```

## Usage

### Run as a script

```bash
python analyze_filings.py --input data/financial_data.csv --output data/financial_analysis_results.csv
```

This prints the full enriched dataset and the per-company summary to the
console, and writes the enriched dataset to `--output` (defaults to
`data/financial_analysis_results.csv`).

### Run as a notebook

```bash
jupyter notebook analyze_filings.ipynb
```

Or open it directly in **VS Code**, **Google Colab**, or **GitHub
Codespaces** — no local install required for Codespaces/Colab. The
notebook walks through the same pipeline as the script, with markdown
explanations at each step and a chart comparing revenue and net margin
trends across the three companies. GitHub also renders `.ipynb` files
natively, so the notebook is viewable directly in the repo without
running anything.

## Metrics explained

| Metric                          | Formula                                      | What it tells you |
|----------------------------------|-----------------------------------------------|--------------------|
| Revenue YoY (%)                  | `(Revenue₁ / Revenue₀ − 1) × 100`             | Top-line growth rate |
| Net Income YoY (%)               | `(Net Income₁ / Net Income₀ − 1) × 100`       | Profit growth rate |
| Operating Cash Flow YoY (%)      | `(OCF₁ / OCF₀ − 1) × 100`                     | Cash generation growth |
| Net Margin (%)                   | `Net Income / Revenue × 100`                  | Profitability per dollar of revenue |
| Operating Cash Flow Margin (%)   | `Operating Cash Flow / Revenue × 100`         | How much revenue converts to cash |
| Liabilities to Assets (%)        | `Total Liabilities / Total Assets × 100`      | Leverage / solvency risk |

## Sample output

```
  Company  Year   Revenue  Net Income  ...  Net Margin (%)  Liabilities to Assets (%)
Microsoft  2023  211915.0     72361.0  ...           34.15                      49.94
Microsoft  2024  245122.0     88136.0  ...           35.95                      48.10
Microsoft  2025  270601.0     96636.0  ...           35.72                      46.85

Company summary:
  Company  Revenue Change (%)  Net Income Change (%)  ...
Microsoft                27.7                    33.5  ...
    Tesla                 ...                     ...  ...
    Apple                 ...                     ...  ...
```

*(Figures above are illustrative — replace `data/financial_data.csv` with
your own extracted values to generate real results.)*

## Methodology notes

- Figures were extracted manually from each company's 10-K filings and
  normalized to consistent units before analysis — no scraping or OCR
  was used at this stage.
- Year-over-year percentages use `pandas.Series.pct_change()`, grouped
  by `Company`, so growth is always calculated within a single company's
  time series, never across companies.
- This analysis is an early step in a larger pipeline. Before feeding
  results into a downstream AI chatbot, data should be re-validated
  against the original filings and checked for restatements, one-time
  items, or fiscal year misalignment (e.g. Apple's fiscal year doesn't
  match the calendar year).

## Roadmap

- [x] Manual data extraction from 10-K filings (2023–2025)
- [x] Pandas pipeline for YoY growth and health indicators
- [x] Jupyter notebook with narrative documentation
- [ ] Automate extraction from EDGAR (e.g. via `sec-edgar-downloader` or the EDGAR full-text search API)
- [ ] Expand to 10-Q (quarterly) filings for more granular trend detection
- [ ] Integrate structured output into an AI-powered financial chatbot (NLP layer)
- [ ] Add automated tests for the calculation functions

## Disclaimer

This project was built as part of a BCG GenAI Consulting simulation
exercise (via Forage) and is for **educational purposes only**. It is
not affiliated with, endorsed by, or reviewed by Boston Consulting
Group, Microsoft, Tesla, or Apple. Figures are manually extracted and
may contain transcription errors — do not use this analysis for actual
investment decisions.

## License

[MIT](LICENSE)
