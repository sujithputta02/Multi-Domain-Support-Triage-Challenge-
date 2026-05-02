import sys
import os
from retrieval.chunker import Chunker
from retrieval.search import SearchEngine
from triage.pipeline import TriagePipeline
import logging

# Setup a minimal logger to console
logging.basicConfig(level=logging.INFO, format='%(message)s')

def main():
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found.")
        return

    print("--- Triage Agent Inspector ---")
    print("Loading corpus and initializing engine (this uses Hybrid Semantic Search)...")
    
    chunker = Chunker(data_dir)
    chunks = chunker.walk_corpus()
    search_engine = SearchEngine(chunks)
    pipeline = TriagePipeline(search_engine)

    print(f"Done! Ingested {len(chunks)} chunks.")
    print("\nYou can now enter a support query to see the agent's logic.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("User Query > ")
        if query.lower() in ['exit', 'quit']:
            break

        ticket = {
            "Issue": query,
            "Subject": "Manual Inspection",
            "Company": "None"
        }

        result = pipeline.process_ticket(ticket)

        print("\n" + "="*50)
        print(f"DOMAIN      : {result['domain']}")
        print(f"INTENT      : {result['request_type']}")
        print(f"PRODUCT AREA: {result['product_area']}")
        print(f"RISK LEVEL  : {result['risk_level']}")
        print(f"DECISION    : {result['decision'].upper()}")
        print(f"REASONING   : {result['justification']}")
        print("-"*50)
        print("FINAL RESPONSE:")
        print(result['response'])
        print("-"*50)
        print("TOP RETRIEVED DOCUMENTS:")
        for doc_id in result['top_docs'][:3]:
            print(f"- {doc_id}")
        print("="*50 + "\n")

if __name__ == "__main__":
    main()
