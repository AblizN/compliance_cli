# ComplianceCLI

A command-line Anti-Money Laundering (AML) and Know Your Customer (KYC)
compliance assistant for compliance officers. Ask questions about financial
regulations or describe a transaction scenario, then ComplianceCLI checks it
against a built-in rules dataset and returns matching rules or violations
instantly.

## Features

- Q&A mode: ask plain-English questions about Anti-Money Laundering (AML) and Know Your Customer (KYC) rules
- Scenario mode: describe a transaction and get violation alerts
- Session logging: every query and result is saved to a log file
- Input validation: rules file is validated on startup

## How to run

```bash
python chatbot.py
```
No external dependencies. Requires Python 3.9+.


## Example interaction

```
6 rules loaded successfully
ComplianceCLI — AML/KYC Assistant
Type your question, or start with 'scenario:' to check a transaction.

You: what is structuring
─────────────────────────────
ID      : AML-002
Category: structuring
Severity: HIGH
Rule    : Breaking up transactions into smaller amounts to avoid
          the $10,000 reporting threshold is illegal and known
          as structuring.
Action  : File a SAR within 30 days.
─────────────────────────────

You: scenario: customer made 3 deposits of 4000 in one day
⚠️  VIOLATION DETECTED
─────────────────────────────
ID      : AML-002
Category: structuring
Severity: HIGH
Rule    : Breaking up transactions into smaller amounts to avoid
          the $10,000 reporting threshold is illegal and known
          as structuring.
Action  : File a SAR within 30 days.
─────────────────────────────

You: who is the president
No matching rules found.

You: exit
Goodbye.
```

## Session log sample

```
[2026-04-20 14:32:01] QUERY: what is structuring | MATCHES: 1
[2026-04-20 14:32:45] QUERY: customer made 3 deposits of 4000 in one day | MATCHES: 1
[2026-04-20 14:33:10] QUERY: who is the president | MATCHES: 0
```

## Project structure

```
ComplianceCLI/
├── chatbot.py        # main application
├── data/
│   └── rules.json    # AML/KYC rules dataset
├── logs/
│   └── .gitkeep      # session logs written here (git-ignored)
└── README.md
```

## Tech stack

- Python 3.9+
- Standard library only: `json`, `datetime`
