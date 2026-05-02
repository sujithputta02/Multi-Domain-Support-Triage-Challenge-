# 🛡️ AI Judge Interview: Deep Prep Guide

## 1. Architectural Strategy
*   **Modular Pipeline**: Explain that you didn't just build a "chatbot." You built a **Triage State Machine**. 
    *   **Phase 1 (Filter)**: Risk screening (Safe first).
    *   **Phase 2 (Route)**: Domain and Product Area detection.
    *   **Phase 3 (Retrieve)**: Hybrid search (Keyword + Semantic).
    *   **Phase 4 (Reason)**: Grounded LLM Response.
*   **Grounding**: The agent uses a "Retrieved-Text-Only" prompt. It is forbidden from using training knowledge.

## 2. Technical Trade-offs
*   **Chunking Strategy**: We used **Section-based chunking** (splitting by `##`). 
    *   *Trade-off*: Smaller chunks are more precise for search but lose context.
    *   *Solution*: We solved this by passing **Multiple Chunks (Top-7)** to the LLM so it can see the surrounding instructions.
*   **Search Alpha (0.5)**: We chose a 50/50 split between BM25 and Semantics. 
    *   *Why?* Semantic-only search was confusing "Pizza" for "Extra Usage." Keywords (BM25) provided the "Anchor" needed to stay on topic.

## 3. Dealing with Edge Cases
*   **The "Pizza" Problem**: How did you handle irrelevant queries?
    *   *Answer*: We implemented a **Semantic Floor**. If the similarity is below 0.25, the system assumes there is no documentation and **Escalates** instead of guessing.
*   **Cross-Domain Contamination**: 
    *   *Answer*: We used **Strict Domain Masking**. Once the classifier says "Visa," the search engine physically cannot see HackerRank or Claude files.

## 4. AI Fluency & Collaboration
*   **Judge Question**: "Did you just let the AI write this?"
*   **Your Answer**: "No. I drove the architecture. For example, when the initial retrieval missed the 'Remove Employee' section, I diagnosed the ranking scores and instructed the AI to build a **Heading-based Boosting Algorithm**. I verified the outputs using a custom **Stress Test Script** that I designed to check Best, Medium, and Worst-case scenarios."

## 5. Failure Modes (Be Honest!)
*   **Latency**: Local LLM performance on low-end hardware.
*   **Vague Queries**: If a user says "I have a problem" with no company name, the agent correctly escalates because it values **Precision over Guesswork**.

---
**Prepared for Sujith Putta | HackerRank Orchestrate 2026**
