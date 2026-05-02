# HackerRank Orchestrate: Multi-Domain Triage Agent

This agent is designed for high-precision, zero-hallucination support ticket triage across HackerRank, Claude, and Visa domains.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- Ollama running locally (`llama3` model installed)
```bash
pip install -r requirements.txt
ollama pull llama3
```

### 2. Run the Triage Pipeline
To process the support tickets and generate the output CSV:
```bash
python3 code/main.py --input support_tickets/support_tickets.csv --output outputs/output.csv
```

### 3. Run the Stress Test
To verify the agent against Best, Medium, Worst, and Edge cases:
```bash
python3 code/stress_test.py
```

### 4. Interactive Inspection
To manually test queries and see internal reasoning:
```bash
python3 code/triage_inspector.py
```

## 🏗️ Architecture
- **Pipeline**: Modular state machine (Classify -> Search -> Generate).
- **Search Engine**: Hybrid BM25 + Semantic Search with **Heading-based Hyper-Boosting**.
- **Safety**: Deterministic Regex Scanner for high-risk ticket escalation.
- **Grounding**: RAG-based generation with a strict semantic floor (0.25) to eliminate hallucinations.

## 🛠️ Key Design Decisions
- **Domain Isolation**: Physical separation of corpus based on detected company.
- **Active Verb Boosting**: Chunks with headers matching query actions (e.g., "Remove") receive a score boost.
- **Context Optimization**: Aggressive cleaning of Markdown metadata to reduce LLM latency.
- **Deterministic Routing**: Hardcoded escalation for fraud, theft, and security vulnerabilities.

---
**Author**: Sujith Putta | HackerRank Orchestrate Hackathon 2026
