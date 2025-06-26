import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin, urlparse
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CUNY1969Scraper:
    def __init__(self, data_dir: str = "../data", assets_dir: str = "../assets"):
        self.data_dir = data_dir
        self.assets_dir = assets_dir
        self.base_url = "https://blogs.baruch.cuny.edu/cuny1969/"
        self.urls = [
            "https://blogs.baruch.cuny.edu/cuny1969/",
            "https://blogs.baruch.cuny.edu/cuny1969/?page_id=1434",
            "https://blogs.baruch.cuny.edu/cuny1969/?page_id=2395",
            "https://blogs.baruch.cuny.edu/cuny1969/?page_id=453"
        ]
        self.scraped_data = []
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
    
    def scrape_page(self, url: str) -> Dict:
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Educational Purpose) CUNY 1969 Research Bot'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('title').text.strip() if soup.find('title') else ''
            
            main_content = soup.find('div', {'class': 'entry-content'}) or soup.find('main') or soup.find('article')
            
            if not main_content:
                main_content = soup.find('body')
            
            text_content = []
            images = []
            
            for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
                text = element.get_text(strip=True)
                if text:
                    text_content.append({
                        'type': element.name,
                        'text': text
                    })
            
            for img in main_content.find_all('img'):
                img_url = urljoin(url, img.get('src', ''))
                alt_text = img.get('alt', '')
                if img_url:
                    img_filename = self.download_image(img_url)
                    if img_filename:
                        images.append({
                            'url': img_url,
                            'alt_text': alt_text,
                            'local_path': img_filename
                        })
            
            return {
                'url': url,
                'title': title,
                'content': text_content,
                'images': images,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def download_image(self, img_url: str) -> str:
        try:
            response = requests.get(img_url, stream=True)
            response.raise_for_status()
            
            filename = os.path.basename(urlparse(img_url).path)
            if not filename:
                filename = f"image_{hash(img_url)}.jpg"
            
            filepath = os.path.join(self.assets_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded image: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error downloading image {img_url}: {e}")
            return None
    
    def scrape_all(self):
        for url in self.urls:
            page_data = self.scrape_page(url)
            if page_data:
                self.scraped_data.append(page_data)
            
            time.sleep(2)
        
        output_file = os.path.join(self.data_dir, 'scraped_content.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Scraped {len(self.scraped_data)} pages. Data saved to {output_file}")
        return self.scraped_data

if __name__ == "__main__":
    scraper = CUNY1969Scraper()
    scraper.scrape_all()