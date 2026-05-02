import os
import sys
from retrieval.chunker import Chunker
from retrieval.search import SearchEngine
from triage.pipeline import TriagePipeline
import pandas as pd

def run_stress_test():
    print("Initializing Stress Test Engine...")
    chunker = Chunker("data")
    chunks = chunker.walk_corpus()
    search_engine = SearchEngine(chunks)
    pipeline = TriagePipeline(search_engine)

    test_cases = [
        # BEST CASES: Clear, direct, documentation exists
        {"category": "BEST", "query": "How do I update my HackerRank password?", "expected": "REPLY (HackerRank)"},
        {"category": "BEST", "query": "What is Amazon Bedrock for Claude?", "expected": "REPLY (Claude)"},
        
        # MEDIUM CASES: Ambiguous phrasing, requires semantic mapping
        {"category": "MEDIUM", "query": "Someone left the company, remove them from hiring account", "expected": "REPLY (HackerRank - Teams)"},
        {"category": "MEDIUM", "query": "I am in a foreign country and my card is not working", "expected": "REPLY (Visa - Travel Support)"},
        
        # WORST CASES: Irrelevant, nonsensical, or noisy
        {"category": "WORST", "query": "I want to order a pepperoni pizza with extra cheese", "expected": "ESCALATE (No documentation)"},
        {"category": "WORST", "query": "Why is the sky blue?", "expected": "ESCALATE (No documentation)"},
        
        # EDGE CASES: Safety and Ambiguity
        {"category": "SAFETY", "query": "My card was stolen and I see unauthorized fraud transactions!", "expected": "ESCALATE (Critical Risk)"},
        {"category": "AMBIGUITY", "query": "how do I login to the portal?", "expected": "ESCALATE (Domain Unknown)"},
        {"category": "CONFLICT", "query": "I used my Visa card to pay for my Claude subscription but it failed", "expected": "Correct Routing to either Visa or Claude"},
    ]

    results = []
    print("\n" + "="*80)
    print(f"{'CATEGORY':<12} | {'QUERY':<40} | {'RESULT':<15}")
    print("-" * 80)

    for case in test_cases:
        ticket = {"Issue": case['query'], "Subject": "Stress Test", "Company": "None"}
        res = pipeline.process_ticket(ticket)
        
        print(f"{case['category']:<12} | {case['query'][:40]:<40} | {res['decision'].upper():<15}")
        results.append({
            "Category": case['category'],
            "Query": case['query'],
            "Decision": res['decision'],
            "Domain": res['domain'],
            "Risk": res['risk_level'],
            "Response_Snippet": res['response'][:100].replace("\n", " ")
        })

    print("="*80)
    
    # Save results to a report
    report_df = pd.DataFrame(results)
    report_path = "outputs/stress_test_report.csv"
    report_df.to_csv(report_path, index=False)
    print(f"\nDeep Stress Test Report saved to: {report_path}")

if __name__ == "__main__":
    run_stress_test()
