import pandas as pd
import subprocess
import sys

# Load the CSV
csv_path = "finance_docs/budget.csv"
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} rows from {csv_path}\n")

# Get the question from the command line
if len(sys.argv) < 2:
    print('Usage: python ask.py "Your question here"')
    sys.exit(1)

question = sys.argv[1]
print(f"Question: {question}\n")

# --- Compute answers with pandas FIRST ---
# This is the key insight: let code do math, let AI do language.

computed_facts = []

# Highest expenses
if "expenses" in question.lower() and ("highest" in question.lower() or "most" in question.lower()):
    expenses_df = df[df["account"] == "Expenses"]
    max_row = expenses_df["actual"].idxmax()
    computed_facts.append(
        f"The month with the highest expenses is {df.loc[max_row, 'period']} "
        f"(row {max_row}), with ${df.loc[max_row, 'actual']:,}."
    )

# Highest revenue
if "revenue" in question.lower() and ("highest" in question.lower() or "most" in question.lower()):
    revenue_df = df[df["account"] == "Revenue"]
    max_row = revenue_df["actual"].idxmax()
    computed_facts.append(
        f"The month with the highest revenue is {df.loc[max_row, 'period']} "
        f"(row {max_row}), with ${df.loc[max_row, 'actual']:,}."
    )

# Where revenue is above budget
if "above budget" in question.lower() or ("revenue" in question.lower() and "budget" in question.lower()):
    above = df[(df["account"] == "Revenue") & (df["actual"] > df["budget"])]
    if len(above) > 0:
        rows = ", ".join(f"[row {i}]" for i in above.index)
        computed_facts.append(
            f"Revenue is above budget in these rows: {rows}."
        )

# --- Build the prompt ---
facts_text = "\n".join(computed_facts) if computed_facts else "(No computed facts for this question.)"

prompt = f"""You are a financial analyst. Answer the question using ONLY the data below.
Cite row numbers like [row 3].
If the data doesn't support the answer, respond with exactly:
INSUFFICIENT EVIDENCE - the data does not support this question.

Computed facts (verified by pandas):
{facts_text}

Full data:
{df.to_string(index=True)}

Question: {question}

Answer:"""

# --- Send to Ollama ---
result = subprocess.run(
    ["ollama", "run", "phi3:mini", prompt],
    capture_output=True,
    text=True
)

print("ANSWER:")
print("=" * 60)
print(result.stdout)
print("=" * 60)