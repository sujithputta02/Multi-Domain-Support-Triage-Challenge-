import pandas as pd
import re
import os

def audit_output(csv_path):
    df = pd.read_csv(csv_path)
    total = len(df)
    results = []
    
    hallucination_count = 0
    cross_domain_count = 0
    
    for idx, row in df.iterrows():
        issue = str(row['Issue']).lower()
        response = str(row['Response']).lower()
        company = str(row['Company']).lower()
        status = row['Status']
        
        if status == 'Replied':
            # 1. Check for cross-domain contamination
            # If the response mentions a different domain's documentation
            other_domains = [d for d in ['hackerrank', 'claude', 'visa'] if d != company]
            for d in other_domains:
                if f"{d}/" in response or f"{d} " in response:
                    # Special check: ensure it's not just part of a generic word
                    if f"reference: {d}" in response or f"source: {d}" in response:
                        cross_domain_count += 1
                        results.append(f"TICKET {idx}: CROSS-DOMAIN detected ({company} ticket using {d} source)")
            
            # 2. Check for "Guessing" language
            guessing_terms = ['i think', 'maybe', 'probably', 'based on my knowledge', 'i assume']
            if any(term in response for term in guessing_terms):
                hallucination_count += 1
                results.append(f"TICKET {idx}: AI GUESSING detected")
                
            # 3. Check for Grounding Reference
            if "reference:" not in response and "source:" not in response:
                hallucination_count += 1
                results.append(f"TICKET {idx}: MISSING REFERENCE (Unfounded answer)")

    # Calculate percentages
    hallucination_pct = (hallucination_count / total) * 100
    cross_domain_pct = (cross_domain_count / total) * 100
    
    print(f"--- FINAL AUDIT REPORT ---")
    print(f"Total Tickets Scanned: {total}")
    print(f"Hallucination Rate: {hallucination_pct:.1f}%")
    print(f"Cross-Domain Contamination Rate: {cross_domain_pct:.1f}%")
    print(f"Status: {'✅ SECURE' if hallucination_pct < 5 else '⚠️ WARNING'}")
    
    if results:
        print("\nDetailed Issues:")
        for r in results:
            print(f"- {r}")

if __name__ == "__main__":
    audit_output("outputs/output.csv")
