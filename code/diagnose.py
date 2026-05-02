import sys, os
sys.path.append(os.path.join(os.getcwd(), 'code'))
from retrieval.chunker import Chunker
from retrieval.search import SearchEngine

chunker = Chunker("data")
chunks = chunker.walk_corpus()
search = SearchEngine(chunks)

queries = [
    ("Someone left the company, remove them from hiring account", "hackerrank"),
    ("I am in a foreign country and my card is not working", "visa"),
    ("How do I update my HackerRank password?", "hackerrank"),
]

for query, domain in queries:
    print(f"\n{'='*80}")
    print(f"QUERY: {query}")
    print(f"DOMAIN: {domain}")
    results = search.search(query, domain=domain, top_k=3)
    if not results:
        print("  NO RESULTS FOUND!")
    for i, r in enumerate(results):
        print(f"  #{i+1} Score={r['score']:.4f} | Title: {r['chunk']['title'][:60]}")
        print(f"       Path: {r['chunk']['path']}")
        print(f"       Text: {r['chunk']['text'][:150]}...")
