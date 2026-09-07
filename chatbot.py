"""
Rule-based financial chatbot prototype for the GFC project.

Answers a small set of predefined queries about a company's financial
performance (Revenue, Net Income, Net Margin, Total Assets) using the
analyzed 10-K data from Task 1 (data/financial_data.csv).

This follows the basic if/elif/else pattern from the task brief:

    def simple_chatbot(user_query):
        if user_query == "What is the total revenue?":
            return "The total revenue is [amount]."
        elif user_query == "How has net income changed over the last year?":
            return "The net income has [increased/decreased] by [amount] over the last year."
        # Add more conditions for other predefined queries
        else:
            return "Sorry, I can only provide information on predefined queries."

...extended so the bracketed placeholders ([amount], [increased/decreased])
are filled in automatically from real data, and so it can answer about any
of the three companies (Microsoft, Tesla, Apple) instead of just one.
"""

from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "financial_data.csv"


def load_data(path=None):
    """Load the analyzed financial data the chatbot draws its answers from."""
    csv_path = Path(path) if path else DATA_PATH
    return pd.read_csv(csv_path)


def format_currency(value):
    return f"${value:,.0f} million"


def _matched_company(query, companies):
    """Find which company (if any) the user mentioned in their query."""
    return next((c for c in companies if c.lower() in query), None)


def _latest_two_years(df, company):
    company_df = df[df["Company"] == company].sort_values("Year")
    return company_df.tail(2)


def simple_chatbot(user_query, df):
    """
    Rule-based chatbot: matches user_query against a small set of predefined
    financial questions and returns an answer built from the analyzed data.
    Falls back to a "Sorry, I can only..." message for anything else,
    exactly like the basic version in the task brief.
    """
    query = user_query.strip().lower()
    companies = df["Company"].unique()
    company = _matched_company(query, companies)

    # 1. "What is the total revenue?"
    if "total revenue" in query and "changed" not in query:
        if not company:
            return "Please specify a company, e.g. \"What is Microsoft's total revenue?\""
        latest = df[df["Company"] == company].sort_values("Year").iloc[-1]
        return (f"The total revenue for {company} in {int(latest['Year'])} "
                f"is {format_currency(latest['Revenue'])}.")

    # 2. "How has net income changed over the last year?"
    elif "net income" in query and "changed" in query:
        if not company:
            return "Please specify a company, e.g. \"How has Tesla's net income changed over the last year?\""
        recent = _latest_two_years(df, company)
        if len(recent) < 2:
            return f"Not enough data to calculate net income change for {company}."
        prev, curr = recent.iloc[0], recent.iloc[1]
        change = curr["Net Income"] - prev["Net Income"]
        direction = "increased" if change >= 0 else "decreased"
        return (f"The net income for {company} has {direction} by "
                f"{format_currency(abs(change))} over the last year "
                f"({int(prev['Year'])} to {int(curr['Year'])}).")

    # 3. "What is the net margin?"
    elif "net margin" in query or "profit margin" in query:
        if not company:
            return "Please specify a company, e.g. \"What is Apple's net margin?\""
        latest = df[df["Company"] == company].sort_values("Year").iloc[-1]
        margin = (latest["Net Income"] / latest["Revenue"]) * 100 if latest["Revenue"] else float("nan")
        return f"{company}'s net margin in {int(latest['Year'])} is {margin:.1f}%."

    # 4. "What are the total assets?"
    elif "total assets" in query:
        if not company:
            return "Please specify a company, e.g. \"What are Microsoft's total assets?\""
        latest = df[df["Company"] == company].sort_values("Year").iloc[-1]
        return (f"{company}'s total assets in {int(latest['Year'])} "
                f"are {format_currency(latest['Total Assets'])}.")

    # 5. "How has revenue changed over the last year?"
    elif "revenue" in query and "changed" in query:
        if not company:
            return "Please specify a company, e.g. \"How has Apple's revenue changed over the last year?\""
        recent = _latest_two_years(df, company)
        if len(recent) < 2:
            return f"Not enough data to calculate revenue change for {company}."
        prev, curr = recent.iloc[0], recent.iloc[1]
        change = curr["Revenue"] - prev["Revenue"]
        direction = "increased" if change >= 0 else "decreased"
        return (f"Revenue for {company} has {direction} by "
                f"{format_currency(abs(change))} over the last year "
                f"({int(prev['Year'])} to {int(curr['Year'])}).")

    else:
        return "Sorry, I can only provide information on predefined queries."


def run_cli(df):
    """Simple command-line loop for interacting with the chatbot."""
    print("Financial Chatbot (type 'exit' to quit)")
    print("Try: \"What is Microsoft's total revenue?\"")
    print("     \"How has Tesla's net income changed over the last year?\"")
    print("     \"What is Apple's net margin?\"")
    while True:
        user_query = input("\nYou: ")
        if user_query.strip().lower() in ("exit", "quit"):
            print("Chatbot: Goodbye!")
            break
        print("Chatbot:", simple_chatbot(user_query, df))


if __name__ == "__main__":
    data = load_data()
    run_cli(data)
