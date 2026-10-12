import pandas as pd
import json
import subprocess
import sys

# Load the CSV
csv_path = "finance_docs/budget.csv"
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} rows from {csv_path}\n")

# Get the question from the command line
if len(sys.argv) < 2:
    print("Usage: python ask.py \"Your question here\"")
    sys.exit(1)

question = sys.argv[1]
print(f"Question: {question}\n")

# Build a text version of the data to give to the AI
data_text = df.to_string(index=True)

# Build the prompt
prompt = f"""You are a financial analyst. Answer the question using ONLY the data below.
Every claim you make must cite the row number in square brackets, like [row 3].
If the data does not contain the answer, respond with exactly:
INSUFFICIENT EVIDENCE - the data does not support this question.

Data:
{data_text}

Question: {question}

Answer (with row citations):"""

# Send to Ollama
result = subprocess.run(
    ["ollama", "run", "phi3:mini", prompt],
    capture_output=True,
    text=True
)

print("ANSWER:")
print("=" * 60)
print(result.stdout)
print("=" * 60)
