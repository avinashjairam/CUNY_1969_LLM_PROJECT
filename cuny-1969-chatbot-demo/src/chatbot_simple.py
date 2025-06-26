import json
import os
from typing import Dict, List, Optional
import re

class SimpleCUNY1969Chatbot:
    """Simplified chatbot without vector database dependencies"""
    
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        self.context_window = []
        self.max_context_items = 5
    
    def load_knowledge_base(self) -> Dict:
        """Load comprehensive knowledge about CUNY 1969"""
        return {
            "events": {
                "1969_protests": "In 1969, students at the City University of New York staged historic protests demanding racial justice and educational equity. The protests began in February when Black and Puerto Rican students entered President Gallagher's office and left 'The Five Demands.' The major occupation occurred on April 22, 1969, when the Black and Puerto Rican Student Community (BPRSC) seized South Campus for two weeks.",
                "timeline": "Key dates: Feb 6 - Five Demands delivered; Feb 13 - Administration Building occupied; April 22 - South Campus seized; May 5 - College reopens after negotiations; May 9 - President Gallagher resigns; May 22 - 'Dual admission' policy agreed.",
                "outcome": "These actions led to the implementation of the groundbreaking Open Admissions policy in 1970 (originally planned for 1975), which dramatically increased access to higher education for Black and Puerto Rican students. The Fall 1970 freshman class was 27% Black and Puerto Rican (up from 13% in 1967)."
            },
            "people": {
                "khadija_deloache": "Khadija DeLoache was a prominent student activist during the 1969 CUNY protests. She played a crucial leadership role and stated: 'We weren't just fighting for ourselves. We were fighting for every Black and Brown student who would come after us.'",
                "robert_marshak": "President Robert Marshak noted that 'The student unrest... was fanned by growing opposition to the disastrous Vietnam War... civil rights movement... attempted to eliminate all perceived manifestations of institutional racism.'",
                "buell_gallagher": "President Buell G. Gallagher was the CUNY president during the 1969 protests. He initially gave ambiguous responses to student demands and resigned on May 9, 1969, after the intense campus unrest.",
                "allen_ballard": "Allen B. Ballard, professor of History and Africana Studies, founded the SEEK program in 1966. He stated: 'I did not want a system in which all the minority students are in the community colleges, and none in the senior colleges.'"
            },
            "demands": {
                "five_demands": "The Five Demands presented in February 1969 were: 1) A separate school of Black and Puerto Rican studies, 2) A separate orientation program for Black and Puerto Rican freshmen, 3) SEEK students to have a voice in program guidelines, 4) Entering class racial composition to reflect NYC high schools, 5) Black and Puerto Rican history and Spanish language required for education majors.",
                "implementation": "Three of the Five Demands were agreed upon by May 5, 1969: establishment of Urban and Ethnic Studies department, Spanish language requirement for education majors, and increased student participation in college governance."
            },
            "programs": {
                "open_admissions": "Open Admissions was adopted in late 1969, guaranteeing admission to the top 50% of high school graduates and students with 80+ averages, with community college slots for other applicants. This increased overall enrollment by approximately 75% and made CUNY reflect the demographic makeup of NYC public high schools.",
                "seek_program": "SEEK (Search for Education, Excellence and Knowledge) was created in 1966 as the nation's first Educational Opportunity Program. Founded by Allen B. Ballard, it welcomed 1,000 minority students in fall 1966, providing supportive programs and extended entrance evaluation for economically and educationally disadvantaged students.",
                "black_puerto_rican_studies": "Black Studies began with 'Negro History and Culture' taught by Dr. Max Yergan. In 1970, the Department of Urban and Ethnic Studies was created, followed by formal Black Studies and Puerto Rican Studies Departments in Fall 1972. Black Studies was chaired by Professor Moyibi J. Amoda, Puerto Rican Studies by Professor Federico Aquino-Bermudez."
            },
            "context": {
                "mlk_impact": "The assassination of Dr. Martin Luther King Jr. on April 4, 1968, had a profound impact on CUNY students, serving as a catalyst for the 1969 protests and pushing students toward more militant tactics.",
                "vietnam_war": "The protests were influenced by growing opposition to the Vietnam War and the broader civil rights movement, as students attempted to eliminate perceived manifestations of institutional racism.",
                "university_of_harlem": "During the occupation, protesters put up a 'University of Harlem' sign on campus to symbolize their vision for the institution as serving the local Harlem community."
            },
            "images": [
                {"alt_text": "Support the Five Demands poster for City College students", "file": "five_demands_poster.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/five_demands_poster-5.jpg"},
                {"alt_text": "CCNY students demonstrating, with a Puerto Rican flag", "file": "ccny_demonstration.png", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/demonstration-1.png"},
                {"alt_text": "City College students and police clashing on West 138th Street", "file": "students_police_clash.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/3-967x1024.jpg"},
                {"alt_text": "University of Harlem sign on campus during the 1969 protests", "file": "university_of_harlem.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/tumblr_nnuwcbEjPv1qzhoqfo1_1280-1.jpg"},
                {"alt_text": "Robert Marshak in 1979, CUNY President during the aftermath", "file": "robert_marshak.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/2-marshak_robert_1979-802x1024.jpg"},
                {"alt_text": "First page of the Five Demands document", "file": "five_demands_doc1.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/wp-content/blogs.dir/21525/files/2022/04/five-demands-1-scaled.jpg"},
                {"alt_text": "Second page of the Five Demands document", "file": "five_demands_doc2.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/wp-content/blogs.dir/21525/files/2022/04/five-demands-2-scaled.jpg"},
                {"alt_text": "CUNY students protesting at Federal Hall in 1989", "file": "cuny_protests_1989.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/6359283579926360351667813250_cuny20protests1.jpg"},
                {"alt_text": "Allen B. Ballard, founder of the SEEK program", "file": "allen_ballard.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/ballard.jpg"},
                {"alt_text": "Department of Black Studies faculty photo from 1973", "file": "black_studies_faculty.jpg", "url": "https://fivedemands.commons.gc.cuny.edu/files/2022/04/black_studies_faculty_1973.jpg"}
            ]
        }
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Simple keyword-based search"""
        query_lower = query.lower()
        results = []
        
        # Search through all knowledge categories
        for category, items in self.knowledge_base.items():
            if category == "images":
                continue
                
            for key, value in items.items():
                if any(word in value.lower() for word in query_lower.split()):
                    results.append({
                        'category': category,
                        'key': key,
                        'content': value
                    })
        
        return results
    
    def get_relevant_images(self, query: str) -> List[Dict]:
        """Get images relevant to query"""
        query_lower = query.lower()
        if any(word in query_lower for word in ['photo', 'image', 'picture', 'show']):
            return self.knowledge_base['images']
        return []
    
    def generate_answer(self, query: str, context: List[Dict]) -> str:
        """Generate answer based on query and context"""
        query_lower = query.lower()
        
        # Direct question handlers
        if "what happened" in query_lower and "1969" in query_lower:
            return self.knowledge_base['events']['1969_protests'] + " " + self.knowledge_base['events']['timeline'] + " " + self.knowledge_base['events']['outcome']
        
        elif "timeline" in query_lower or "chronology" in query_lower:
            return self.knowledge_base['events']['timeline'] + " The protests culminated in President Gallagher's resignation and the 'dual admission' policy that evolved into Open Admissions."
        
        elif "khadija deloache" in query_lower or "who was khadija" in query_lower:
            return self.knowledge_base['people']['khadija_deloache']
        
        elif "robert marshak" in query_lower or "marshak" in query_lower:
            return self.knowledge_base['people']['robert_marshak']
        
        elif "gallagher" in query_lower or "buell gallagher" in query_lower:
            return self.knowledge_base['people']['buell_gallagher']
        
        elif "allen ballard" in query_lower or "ballard" in query_lower:
            return self.knowledge_base['people']['allen_ballard']
        
        elif "five demands" in query_lower:
            return self.knowledge_base['demands']['five_demands'] + " " + self.knowledge_base['demands']['implementation']
        
        elif "open admissions" in query_lower or "open admission" in query_lower:
            return self.knowledge_base['programs']['open_admissions']
        
        elif "seek" in query_lower and "program" in query_lower:
            return self.knowledge_base['programs']['seek_program']
        
        elif "black studies" in query_lower or "puerto rican studies" in query_lower:
            return self.knowledge_base['programs']['black_puerto_rican_studies']
        
        elif "university of harlem" in query_lower:
            return self.knowledge_base['context']['university_of_harlem']
        
        elif "vietnam war" in query_lower or "vietnam" in query_lower:
            return self.knowledge_base['context']['vietnam_war']
        
        elif "mlk" in query_lower or "martin luther king" in query_lower:
            return self.knowledge_base['context']['mlk_impact']
        
        elif any(word in query_lower for word in ['photo', 'image', 'show']):
            return "Here are authentic historical images from the 1969 CUNY protests and related events: The original 'Support the Five Demands' poster, CCNY students demonstrating with Puerto Rican flags, confrontations between students and police on West 138th Street, the 'University of Harlem' sign, President Robert Marshak, the actual Five Demands documents, SEEK program founder Allen B. Ballard, Black Studies faculty from 1973, and continuing protests at Federal Hall in 1989."
        
        # Fallback to context-based answer
        elif context:
            return context[0]['content']
        
        return "I couldn't find specific information about that in the CUNY 1969 archives. Try asking about the protests, timeline, Five Demands, key figures like Gallagher or Marshak, Open Admissions, SEEK program, or Black and Puerto Rican Studies."
    
    def chat(self, user_input: str) -> Dict:
        """Main chat interface"""
        # Search for relevant content
        search_results = self.search_knowledge(user_input)
        images = self.get_relevant_images(user_input)
        
        # Generate answer
        answer = self.generate_answer(user_input, search_results)
        
        # Store in context
        self.context_window.append({
            'query': user_input,
            'response': answer
        })
        
        if len(self.context_window) > self.max_context_items:
            self.context_window.pop(0)
        
        return {
            'answer': answer,
            'sources': [
                'https://fivedemands.commons.gc.cuny.edu/',
                'https://fivedemands.commons.gc.cuny.edu/timeline/',
                'https://fivedemands.commons.gc.cuny.edu/seek-and-you-shall-find-a-search-for-education-excellence-and-knowledge/',
                'https://fivedemands.commons.gc.cuny.edu/black-and-puerto-rican-studies/',
                'https://fivedemands.commons.gc.cuny.edu/closing-the-open-door-open-admissions-at-the-city-university-of-new-york/'
            ],
            'images': images
        }
    
    def get_demo_questions(self) -> List[str]:
        """Get list of demo questions"""
        return [
            "What happened at CUNY in 1969?",
            "What were the Five Demands?",
            "Show me photos from the protests",
            "Tell me about the timeline of events",
            "What was the SEEK program?",
            "Who was President Gallagher?",
            "What is Open Admissions?",
            "Tell me about Black and Puerto Rican Studies",
            "Who was Allen Ballard?",
            "What was the University of Harlem sign?"
        ]