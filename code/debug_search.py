import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'code'))
from retrieval.chunker import Chunker
from retrieval.search import SearchEngine

def debug():
    chunker = Chunker("data")
    chunks = chunker.walk_corpus()
    search = SearchEngine(chunks)
    
    query = "I want to order a pepperoni pizza with extra cheese"
    print(f"DEBUGGING QUERY: {query}")
    results = search.search(query, top_k=3)
    
    for r in results:
        print(f"Score: {r['score']:.4f} | Path: {r['chunk']['path']}")
        print(f"Content Snippet: {r['chunk']['content'][:100]}...")
        print("-" * 20)

if __name__ == "__main__":
    debug()
