# Financial Chatbot — Documentation

## How it works

`chatbot.py` is a rule-based prototype that answers a small set of
predefined financial questions using the data extracted and analyzed in
Task 1 (`data/financial_data.csv`).

It follows a simple `if / elif / else` pattern: the user's query is
checked against a list of known question patterns (e.g. "total revenue",
"net income ... changed"), and if a match is found, the chatbot looks up
the relevant figures for the mentioned company and fills them into a
response template. If no pattern matches, it returns a fallback message
telling the user it can only answer predefined queries — the same
fallback behavior shown in the original task brief.

Unlike a purely hardcoded version (with a single fixed answer per
question), this version pulls the actual numbers from the loaded CSV each
time, so the amounts and directions ("increased"/"decreased") are always
computed from real data rather than typed in by hand.

## Predefined queries it can answer

For **Microsoft**, **Tesla**, or **Apple** (just include the company name
in your question):

1. **"What is [Company]'s total revenue?"**
   Returns the most recent year's total revenue.
2. **"How has [Company]'s net income changed over the last year?"**
   Compares the two most recent years and reports the dollar change and
   direction (increased/decreased).
3. **"What is [Company]'s net margin?"**
   Returns Net Income ÷ Revenue for the most recent year, as a percentage.
4. **"What are [Company]'s total assets?"**
   Returns the most recent year's total assets.
5. **"How has [Company]'s revenue changed over the last year?"**
   Compares the two most recent years and reports the dollar change and
   direction.

Example:

```
You: What is Microsoft's total revenue?
Chatbot: The total revenue for Microsoft in 2025 is $260,000 million.
```

## Data

The chatbot loads `data/financial_data.csv`, expecting the columns
`Company`, `Year`, `Revenue`, `Net Income`, `Total Assets`,
`Total Liabilities`, `Operating Cash Flow` — the same schema produced in
Task 1.

For this submission's test run, `data/example_data.csv` (clearly
illustrative sample figures, not real filed numbers) was used instead, so
the chatbot's behavior could be demonstrated without depending on
manually transcribed real 10-K values being finalized. To run it against
real filings data, swap in the completed `financial_data.csv` from Task 1
— no code changes needed.

## Limitations

- **Exact keyword matching, not true NLP.** The chatbot looks for
  specific phrases ("total revenue", "net income", "changed", etc.) and
  a company name. Rephrased or unrelated questions ("Is Microsoft a good
  investment?") will hit the fallback response, even if they're
  financially related.
- **No conversation memory.** Each query is answered independently; the
  chatbot doesn't remember a company mentioned in a previous question, so
  the user must name the company in every query.
- **Only the most recent year (or most recent two years) is used** for
  "current" and "change" queries — it doesn't yet support arbitrary
  year-to-year comparisons (e.g. "compare 2023 to 2025").
- **No error correction for typos** in company names or misspelled
  metrics.
- **Not a production system.** This is a prototype demonstrating
  rule-based logic and data integration principles, not a chatbot ready
  for real users — a production version would need real NLP (e.g. intent
  classification), broader query coverage, and proper testing.

## Possible next steps

- Add lightweight NLP (e.g. simple synonym matching or an intent
  classifier) so rephrased questions still match.
- Add state management so a company mentioned once is remembered for
  follow-up questions.
- Expand to support explicit year comparisons and 10-Q (quarterly) data.
