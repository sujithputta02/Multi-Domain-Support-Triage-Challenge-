import os
import argparse
import pandas as pd
import logging
from retrieval.chunker import Chunker
from retrieval.search import SearchEngine
from triage.pipeline import TriagePipeline
from utils.io import load_csv, save_csv, save_json
from tqdm import tqdm

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main():
    parser = argparse.ArgumentParser(description="Multi-Domain Support Triage Agent")
    parser.add_argument("--input", default="support_tickets/support_tickets.csv", help="Input CSV file")
    parser.add_argument("--output", default="outputs/output.csv", help="Output CSV file")
    parser.add_argument("--log", default="outputs/log.txt", help="Log file")
    parser.add_argument("--data", default="data", help="Corpus directory")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    setup_logging(args.log)
    logger = logging.getLogger('main')

    logger.info("Starting ingestion...")
    chunker = Chunker(args.data)
    chunks = chunker.walk_corpus()
    logger.info(f"Ingested {len(chunks)} chunks.")

    logger.info("Initializing search engine...")
    search_engine = SearchEngine(chunks)

    logger.info("Initializing pipeline...")
    pipeline = TriagePipeline(search_engine)

    logger.info(f"Loading tickets from {args.input}...")
    df = load_csv(args.input)
    
    results = []
    logger.info(f"Processing {len(df)} tickets...")
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        ticket = row.to_dict()
        ticket['ticket_id'] = idx # Use index as ID if not present
        
        try:
            result = pipeline.process_ticket(ticket)
            results.append(result)
            
            # Log individual ticket results for the transcript
            logger.info(f"Ticket {idx} | Domain: {result['domain']} | Decision: {result['decision']}")
            logger.info(f"Justification: {result['justification']}")
            logger.info("-" * 40)
        except Exception as e:
            logger.error(f"Error processing ticket {idx}: {e}")
            results.append({
                "ticket_id": idx,
                "domain": "unknown",
                "decision": "escalate",
                "response": "An error occurred during processing.",
                "justification": str(e)
            })

    # Prepare output CSV
    output_df = df.copy()
    domain_map = {'hackerrank': 'HackerRank', 'claude': 'Claude', 'visa': 'Visa', 'unknown': 'None'}
    output_df['Company'] = [domain_map.get(r['domain'], 'None') for r in results]
    output_df['Status'] = ['Replied' if r['decision'] == 'reply' else 'Escalated' for r in results]
    output_df['Response'] = [r['response'] for r in results]
    output_df['Request Type'] = [r.get('request_type', 'unknown') for r in results]
    output_df['Product Area'] = [r.get('product_area', 'unknown') for r in results]
    
    # Match sample columns: Issue,Subject,Company,Response,Product Area,Status,Request Type
    output_df = output_df[['Issue', 'Subject', 'Company', 'Response', 'Product Area', 'Status', 'Request Type']]

    logger.info(f"Saving results to {args.output}...")
    save_csv(output_df, args.output)
    
    logger.info("Done.")

if __name__ == "__main__":
    main()
