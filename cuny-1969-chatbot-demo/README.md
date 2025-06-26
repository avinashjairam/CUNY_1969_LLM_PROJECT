# CUNY 1969 Historical Chatbot Demo

An interactive chatbot that helps users explore the historic 1969 student protests at the City University of New York (CUNY). This demo uses retrieval-augmented generation (RAG) with local models to answer questions about this pivotal moment in educational history.

## Features

- **Interactive Q&A**: Ask questions about the 1969 CUNY protests and receive contextual answers
- **Historical Images**: View relevant historical photos when asking about visual content
- **Source Citations**: All answers include references to source materials
- **Local Processing**: Runs entirely locally without requiring external API keys
- **Demo Questions**: Pre-configured questions to showcase the chatbot's capabilities

## Project Structure

```
cuny-1969-chatbot-demo/
├── src/
│   ├── scraper.py          # Web scraping module for CUNY archives
│   ├── knowledge_base.py   # Vector database and semantic search
│   ├── demo_data.py        # Demo data creation for testing
│   └── chatbot.py          # RAG chatbot implementation
├── data/
│   ├── scraped_content.json    # Scraped/demo content
│   ├── sample_qa_pairs.json    # Test Q&A pairs
│   └── chroma_db/              # Vector database storage
├── assets/                     # Downloaded images
├── demo/
│   ├── app.py              # Streamlit interface
│   └── run_demo.py         # Command-line demo script
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cuny-1969-chatbot-demo
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the demo data**:
   ```bash
   cd src
   python demo_data.py
   python chatbot.py  # This will build the knowledge base
   cd ..
   ```

## Running the Demo

### Streamlit Web Interface (Recommended)

```bash
cd demo
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Command-Line Demo

```bash
cd demo
python run_demo.py
```

## Sample Questions to Try

1. **"What happened at CUNY in 1969?"**
   - Learn about the protests and their significance

2. **"Who was Khadija DeLoache?"**
   - Discover key figures in the protest movement

3. **"What were the Five Demands?"**
   - Understand the specific changes students demanded

4. **"Show me photos from the protests"**
   - View historical images from the archives

5. **"How did MLK's death affect CUNY students?"**
   - Explore the broader civil rights context

## Technical Details

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Database**: ChromaDB for semantic search
- **Text Processing**: BeautifulSoup4 for web scraping
- **UI Framework**: Streamlit for web interface
- **Image Handling**: PIL/Pillow for image display

## Demo Limitations

- Uses pre-generated demo data for consistent demonstrations
- Limited to specific historical content about CUNY 1969
- Images are placeholder references (actual scraping would download real images)
- Runs locally without advanced language models

## Development

To extend the chatbot:

1. Add more content to `demo_data.py`
2. Implement actual web scraping by running `scraper.py`
3. Enhance the answer generation in `chatbot.py`
4. Add more interactive features to `demo/app.py`

## Requirements

- Python 3.8 or higher
- 4GB RAM minimum
- ~100MB disk space

## License

This project is for educational and demonstration purposes, showcasing RAG technology applied to historical content.

## Acknowledgments

Content based on the CUNY 1969 digital archives documenting the historic student protests that transformed access to higher education.