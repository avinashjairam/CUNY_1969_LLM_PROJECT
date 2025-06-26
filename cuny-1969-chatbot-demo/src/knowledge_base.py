import json
import os
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CUNY1969KnowledgeBase:
    def __init__(self, data_dir: str = "../data", db_dir: str = "../data/chroma_db"):
        self.data_dir = data_dir
        self.db_dir = db_dir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=self.db_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="cuny_1969_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def chunk_text(self, text: str, chunk_size: int = 300) -> List[str]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def extract_metadata(self, content: Dict) -> Dict:
        metadata = {
            'source_url': content.get('url', ''),
            'title': content.get('title', ''),
            'scraped_at': content.get('scraped_at', '')
        }
        
        text_content = ' '.join([item['text'] for item in content.get('content', [])])
        
        people_patterns = [
            r'\b(?:Dr\.|Professor|Prof\.|Mr\.|Mrs\.|Ms\.)?\s*[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'Khadija DeLoache',
            r'MLK|Martin Luther King'
        ]
        
        people = set()
        for pattern in people_patterns:
            matches = re.findall(pattern, text_content)
            people.update(matches)
        
        metadata['people_mentioned'] = list(people)[:10]
        
        date_pattern = r'\b(?:19\d{2}|20\d{2})\b'
        dates = re.findall(date_pattern, text_content)
        metadata['dates_mentioned'] = list(set(dates))[:5]
        
        return metadata
    
    def load_scraped_data(self):
        scraped_file = os.path.join(self.data_dir, 'scraped_content.json')
        
        if not os.path.exists(scraped_file):
            logger.warning(f"Scraped content file not found: {scraped_file}")
            return []
        
        with open(scraped_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def build_knowledge_base(self):
        scraped_data = self.load_scraped_data()
        
        if not scraped_data:
            logger.warning("No scraped data found")
            return
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for idx, page_data in enumerate(scraped_data):
            full_text = '\n'.join([item['text'] for item in page_data.get('content', [])])
            
            chunks = self.chunk_text(full_text)
            
            base_metadata = self.extract_metadata(page_data)
            
            for chunk_idx, chunk in enumerate(chunks):
                chunk_metadata = base_metadata.copy()
                chunk_metadata['chunk_index'] = chunk_idx
                chunk_metadata['total_chunks'] = len(chunks)
                chunk_metadata['content_type'] = 'text'
                
                all_chunks.append(chunk)
                all_metadatas.append(chunk_metadata)
                all_ids.append(f"page_{idx}_chunk_{chunk_idx}")
            
            for img_idx, image in enumerate(page_data.get('images', [])):
                img_metadata = base_metadata.copy()
                img_metadata['content_type'] = 'image'
                img_metadata['image_url'] = image['url']
                img_metadata['image_local_path'] = image['local_path']
                
                img_text = f"Image: {image['alt_text']} (from {page_data['title']})"
                
                all_chunks.append(img_text)
                all_metadatas.append(img_metadata)
                all_ids.append(f"page_{idx}_img_{img_idx}")
        
        if all_chunks:
            self.collection.add(
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            
            logger.info(f"Added {len(all_chunks)} chunks to knowledge base")
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return {
            'query': query,
            'results': formatted_results
        }
    
    def get_images_by_query(self, query: str, n_results: int = 3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results * 3,
            where={"content_type": "image"}
        )
        
        images = []
        for i in range(len(results['documents'][0])):
            if len(images) >= n_results:
                break
            
            metadata = results['metadatas'][0][i]
            if metadata.get('content_type') == 'image':
                images.append({
                    'alt_text': results['documents'][0][i],
                    'local_path': metadata.get('image_local_path', ''),
                    'source_url': metadata.get('source_url', ''),
                    'image_url': metadata.get('image_url', '')
                })
        
        return images

if __name__ == "__main__":
    kb = CUNY1969KnowledgeBase()
    kb.build_knowledge_base()
    
    test_results = kb.search("What happened at CUNY in 1969?")
    print(f"Found {len(test_results['results'])} results")