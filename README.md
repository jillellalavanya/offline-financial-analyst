# Offline AI Financial Analyst

A fully offline AI tool that reads financial CSV data and answers natural-language questions with row-level citations — no cloud, no API keys, no data leaving your machine.

## Problem Statement

Financial analysts and their clients often need AI-powered insights from sensitive financial data, but cloud-based AI tools require uploading that data to third-party servers. For many businesses, this creates unacceptable privacy, compliance, and data-residency risks.

This project solves that: a fully offline financial analyst that runs on a consumer laptop, keeps all data local, and produces audit-ready answers that cite the exact rows they came from.

## How It Works

1. Ollama — Runs a small language model (Phi-3 Mini) locally
2. pandas — Reads the CSV financial data
3. ask.py — A Python script that glues them together with citation enforcement

### Query Flow

1. You ask a question in plain English
2. The script loads the CSV and builds a prompt
3. The prompt includes the data and strict citation rules
4. Ollama generates an answer using only that data
5. Every claim includes a [row N] citation
6. If the data doesn't support the answer, the AI says INSUFFICIENT EVIDENCE

## Tech Stack

- AI Engine: Ollama
- Model: Phi-3 Mini (quantized)
- Language: Python 3.12
- Data Layer: pandas
- Interface: Terminal / CLI

## Installation

### Prerequisites

- Python 3.11+
- Ollama installed (ollama.com)
- 8 GB RAM minimum

### Setup

1. Clone the repo
2. Create a virtual environment: python3.12 -m venv .venv
3. Activate it: source .venv/bin/activate
4. Install pandas: pip install pandas
5. Pull the model: ollama pull phi3:mini

## Usage

Run: python ask.py "Where is revenue above budget?"

### Example Output

Loaded 12 rows from finance_docs/budget.csv

Question: Where is revenue above budget?

ANSWER:
Revenue is above budget in the following months as per row [2], [4], [8], and [10].

### Refusal Example

Run: python ask.py "What was the marketing spend in December?"

ANSWER:
INSUFFICIENT EVIDENCE - the data does not support this question.

## Why This Matters

- Fully offline: No data leaves your machine
- Cited answers: Every claim traces to a specific row
- Refusal on insufficient evidence: No hallucinated numbers
- Consumer hardware: Runs on any modern laptop
- Free and open source: No subscriptions or API costs

## Skills Demonstrated

- Local LLM inference (Ollama)
- Prompt engineering for financial Q&A
- Citation enforcement and hallucination mitigation
- Privacy-preserving AI architecture
- Python, pandas, CLI tooling

## License

MIT