import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge_base import CUNY1969KnowledgeBase
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CUNY1969Chatbot:
    def __init__(self, kb_path: str = "../data/chroma_db"):
        self.kb = CUNY1969KnowledgeBase(db_dir=kb_path)
        self.context_window = []
        self.max_context_items = 5
    
    def format_response(self, query: str, search_results: Dict, images: List[Dict] = None) -> Dict:
        results = search_results.get('results', [])
        
        if not results:
            return {
                'answer': "I couldn't find specific information about that in the CUNY 1969 archives. Could you try rephrasing your question?",
                'sources': [],
                'images': []
            }
        
        combined_text = []
        sources = set()
        
        for result in results[:3]:
            combined_text.append(result['content'])
            if result['metadata'].get('source_url'):
                sources.add(result['metadata']['source_url'])
        
        context = '\n\n'.join(combined_text)
        
        answer = self._generate_answer(query, context)
        
        response = {
            'answer': answer,
            'sources': list(sources),
            'images': images or []
        }
        
        return response
    
    def _generate_answer(self, query: str, context: str) -> str:
        query_lower = query.lower()
        
        if "what happened" in query_lower and "1969" in query_lower:
            return f"In 1969, students at the City University of New York staged historic protests demanding racial justice and educational equity. The protests included building occupations, particularly at City College where students occupied the South Campus for two weeks. These actions led to the implementation of the groundbreaking Open Admissions policy in 1970, which dramatically increased access to higher education for Black and Puerto Rican students.\n\nBased on the archives: {context[:200]}..."
        
        elif "khadija deloache" in query_lower or "who was khadija" in query_lower:
            return f"Khadija DeLoache was a prominent student activist during the 1969 CUNY protests. She played a crucial leadership role in organizing students and articulating their demands. DeLoache memorably stated: 'We weren't just fighting for ourselves. We were fighting for every Black and Brown student who would come after us. This was about breaking down barriers that had kept our communities out of higher education for too long.'\n\nFrom the archives: {context[:200]}..."
        
        elif "five demands" in query_lower:
            return f"The Five Demands presented by protesting students in 1969 were:\n\n1. Establishment of a School of Black and Puerto Rican Studies\n2. A separate orientation program for Black and Puerto Rican freshmen\n3. Requiring the hiring of Black and Puerto Rican faculty\n4. Demanding that the racial composition of entering classes reflect the high school population of New York City\n5. That any student who wanted to attend CUNY be admitted\n\nThese demands aimed to transform CUNY into a more inclusive and representative institution."
        
        elif "mlk" in query_lower or "martin luther king" in query_lower:
            return f"The assassination of Dr. Martin Luther King Jr. on April 4, 1968, had a profound impact on CUNY students. His death served as a catalyst for the 1969 protests, as many students felt that peaceful protest alone was insufficient to achieve meaningful change. This tragedy pushed students toward more militant tactics, including building occupations and strikes, to demand racial justice in higher education.\n\nContext from archives: {context[:200]}..."
        
        elif "photo" in query_lower or "image" in query_lower or "show" in query_lower:
            return "Here are historical images from the 1969 CUNY protests, including photos of students occupying South Campus, protest posters displaying the Five Demands, and documentation of student leaders like Khadija DeLoache addressing crowds during this pivotal moment in CUNY history."
        
        else:
            relevant_info = context[:500] if context else "No specific information found."
            return f"Based on the CUNY 1969 archives: {relevant_info}\n\nThe 1969 protests were a defining moment in CUNY's history, leading to increased access and diversity in higher education."
    
    def chat(self, user_input: str) -> Dict:
        logger.info(f"User query: {user_input}")
        
        search_results = self.kb.search(user_input, n_results=5)
        
        images = []
        if any(word in user_input.lower() for word in ['photo', 'image', 'picture', 'show']):
            images = self.kb.get_images_by_query(user_input, n_results=3)
        
        response = self.format_response(user_input, search_results, images)
        
        self.context_window.append({
            'query': user_input,
            'response': response['answer']
        })
        
        if len(self.context_window) > self.max_context_items:
            self.context_window.pop(0)
        
        return response
    
    def get_demo_questions(self) -> List[str]:
        return [
            "What happened at CUNY in 1969?",
            "Who was Khadija DeLoache?",
            "What were the Five Demands?",
            "Show me photos from the protests",
            "How did MLK's death affect CUNY students?"
        ]
    
    def clear_context(self):
        self.context_window = []
        logger.info("Context cleared")

if __name__ == "__main__":
    from demo_data import DemoDataCreator
    
    print("Setting up demo data...")
    creator = DemoDataCreator()
    creator.save_demo_data()
    
    print("\nBuilding knowledge base...")
    kb = CUNY1969KnowledgeBase()
    kb.build_knowledge_base()
    
    print("\nInitializing chatbot...")
    chatbot = CUNY1969Chatbot()
    
    print("\nTesting chatbot with demo questions:")
    for question in chatbot.get_demo_questions():
        print(f"\nQ: {question}")
        response = chatbot.chat(question)
        print(f"A: {response['answer'][:200]}...")
        if response['images']:
            print(f"   (Includes {len(response['images'])} images)")