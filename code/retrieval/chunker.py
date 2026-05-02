import os
import re
from pathlib import Path

class Chunker:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)

    def walk_corpus(self):
        chunks = []
        for domain_dir in self.data_dir.iterdir():
            if domain_dir.is_dir():
                domain = domain_dir.name
                for file_path in domain_dir.rglob('*.md'):
                    relative_path = file_path.relative_to(self.data_dir)
                    content = file_path.read_text(encoding='utf-8')
                    
                    # Extract title from filename or first H1
                    title = file_path.stem.replace('-', ' ').title()
                    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    if h1_match:
                        title = h1_match.group(1).strip()
                    
                    # Simple chunking: by section or paragraph
                    sections = re.split(r'\n(?=#{1,3}\s)', content)
                    for i, section in enumerate(sections):
                        if not section.strip():
                            continue
                        
                        chunk_id = f"{domain}_{relative_path.as_posix().replace('/', '_')}_{i}"
                        # Repeat title to increase keyword/semantic weight
                        indexed_content = f"Title: {title}\nTitle: {title}\nDomain: {domain}\n\n{section.strip()}"
                        chunks.append({
                            "chunk_id": chunk_id,
                            "domain": domain,
                            "title": title,
                            "path": str(relative_path),
                            "text": section.strip(),
                            "content": indexed_content
                        })
        return chunks
