"""Pandas analysis for the SEC 10-K financial dataset."""

from pathlib import Path
import argparse
import pandas as pd

METRICS = [
    "Revenue",
    "Net Income",
    "Total Assets",
    "Total Liabilities",
    "Operating Cash Flow",
]


def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load and validate the normalized filing data."""
    csv_path = Path(path) if path else Path(__file__).parent / "data" / "financial_data.csv"
    frame = pd.read_csv(csv_path)
    required = {"Company", "Year", *METRICS}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return frame.sort_values(["Company", "Year"]).reset_index(drop=True)


def calculate_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    """Add year-over-year changes and financial health indicators."""
    result = frame.copy()
    grouped = result.groupby("Company", sort=False)
    for metric in ["Revenue", "Net Income", "Operating Cash Flow"]:
        result[f"{metric} YoY (%)"] = grouped[metric].pct_change().mul(100).round(2)
    result["Net Margin (%)"] = result["Net Income"].div(result["Revenue"]).mul(100).round(2)
    result["Operating Cash Flow Margin (%)"] = (
        result["Operating Cash Flow"].div(result["Revenue"]).mul(100).round(2)
    )
    result["Liabilities to Assets (%)"] = (
        result["Total Liabilities"].div(result["Total Assets"]).mul(100).round(2)
    )
    return result


def company_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize first-to-last year changes by company."""
    ordered = frame.sort_values(["Company", "Year"])
    first = ordered.groupby("Company").first()
    last = ordered.groupby("Company").last()
    summary = pd.DataFrame(index=first.index)
    for metric in METRICS:
        summary[f"{metric} Change (%)"] = (
            last[metric].div(first[metric]).sub(1).mul(100).round(2)
        )
    return summary.reset_index()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    analyzed = calculate_metrics(load_data(args.input))
    output = args.output or Path(__file__).parent / "data" / "financial_analysis_results.csv"
    analyzed.to_csv(output, index=False)
    print(analyzed.to_string(index=False))
    print("\nCompany summary:")
    print(company_summary(analyzed).to_string(index=False))


if __name__ == "__main__":
    main()
