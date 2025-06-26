import json
import os
from typing import Dict, List

class DemoDataCreator:
    def __init__(self, data_dir: str = "../data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    
    def create_demo_content(self) -> List[Dict]:
        demo_content = [
            {
                "url": "https://blogs.baruch.cuny.edu/cuny1969/demo",
                "title": "CUNY 1969: Key Facts and Events",
                "content": [
                    {
                        "type": "h1",
                        "text": "The 1969 CUNY Student Protests"
                    },
                    {
                        "type": "p",
                        "text": "In 1969, students at the City University of New York staged a series of protests that would transform the university forever. The protests were sparked by the assassination of Dr. Martin Luther King Jr. in April 1968 and growing demands for racial justice in higher education."
                    },
                    {
                        "type": "h2",
                        "text": "The Five Demands"
                    },
                    {
                        "type": "p",
                        "text": "The protesting students presented five key demands to the CUNY administration: 1) Establishment of a School of Black and Puerto Rican Studies, 2) A separate orientation program for Black and Puerto Rican freshmen, 3) Requiring the hiring of Black and Puerto Rican faculty, 4) Demanding that the racial composition of entering classes reflect the high school population of New York City, 5) That any student who wanted to attend CUNY be admitted."
                    },
                    {
                        "type": "h2",
                        "text": "Key Figures: Khadija DeLoache"
                    },
                    {
                        "type": "p",
                        "text": "Khadija DeLoache, a student activist, played a crucial role in the protests. She famously said: 'We weren't just fighting for ourselves. We were fighting for every Black and Brown student who would come after us. This was about breaking down barriers that had kept our communities out of higher education for too long.'"
                    },
                    {
                        "type": "p",
                        "text": "The protests at City College began on April 22, 1969, when students occupied the South Campus. The occupation lasted for two weeks, with students renaming buildings after Malcolm X, Che Guevara, and other revolutionary figures."
                    },
                    {
                        "type": "h2",
                        "text": "Impact of MLK's Death"
                    },
                    {
                        "type": "p",
                        "text": "The assassination of Martin Luther King Jr. on April 4, 1968, profoundly affected CUNY students. Many felt that peaceful protest alone was not enough to achieve meaningful change. This sentiment fueled the more militant approach taken during the 1969 protests."
                    },
                    {
                        "type": "h2",
                        "text": "Open Admissions Policy"
                    },
                    {
                        "type": "p",
                        "text": "The most significant outcome of the 1969 protests was the implementation of the Open Admissions policy in 1970. This policy guaranteed admission to CUNY for all New York City high school graduates, dramatically increasing access to higher education for Black and Puerto Rican students."
                    },
                    {
                        "type": "p",
                        "text": "The protests involved thousands of students across multiple CUNY campuses, including City College, Brooklyn College, and Queens College. The movement represented a watershed moment in the struggle for educational equity."
                    }
                ],
                "images": [
                    {
                        "url": "https://blogs.baruch.cuny.edu/cuny1969/files/protest_south_campus.jpg",
                        "alt_text": "Students occupying South Campus at City College during the 1969 protests",
                        "local_path": "protest_south_campus.jpg"
                    },
                    {
                        "url": "https://blogs.baruch.cuny.edu/cuny1969/files/five_demands_poster.jpg",
                        "alt_text": "Poster displaying the Five Demands of the protesting students",
                        "local_path": "five_demands_poster.jpg"
                    },
                    {
                        "url": "https://blogs.baruch.cuny.edu/cuny1969/files/khadija_deloache_speaking.jpg",
                        "alt_text": "Khadija DeLoache speaking to fellow protesters during the occupation",
                        "local_path": "khadija_deloache_speaking.jpg"
                    }
                ],
                "scraped_at": "2024-01-01 12:00:00"
            }
        ]
        
        return demo_content
    
    def create_sample_qa_pairs(self) -> List[Dict]:
        qa_pairs = [
            {
                "question": "What happened at CUNY in 1969?",
                "expected_answer": "In 1969, students at CUNY staged protests demanding racial justice in higher education. The protests led to the occupation of buildings and resulted in the implementation of Open Admissions policy.",
                "keywords": ["protests", "1969", "occupation", "racial justice", "Open Admissions"]
            },
            {
                "question": "Who was Khadija DeLoache?",
                "expected_answer": "Khadija DeLoache was a student activist who played a crucial role in the 1969 CUNY protests. She emphasized that they were fighting for future generations of Black and Brown students.",
                "keywords": ["Khadija DeLoache", "student activist", "Black and Brown students"]
            },
            {
                "question": "What were the Five Demands?",
                "expected_answer": "The Five Demands included: School of Black and Puerto Rican Studies, separate orientation programs, hiring of Black and Puerto Rican faculty, racial composition reflecting NYC high schools, and open admission for all who wanted to attend.",
                "keywords": ["Five Demands", "Black and Puerto Rican Studies", "faculty", "racial composition", "open admission"]
            },
            {
                "question": "Show me photos from the protests",
                "expected_answer": "Images should show students occupying South Campus, Five Demands poster, and Khadija DeLoache speaking.",
                "keywords": ["photos", "images", "protests", "South Campus", "occupation"]
            },
            {
                "question": "How did MLK's death affect CUNY students?",
                "expected_answer": "MLK's assassination in April 1968 profoundly affected CUNY students, leading many to believe that peaceful protest alone was insufficient, which fueled the more militant approach in 1969.",
                "keywords": ["MLK", "Martin Luther King", "assassination", "1968", "militant approach"]
            }
        ]
        
        return qa_pairs
    
    def save_demo_data(self):
        demo_content = self.create_demo_content()
        qa_pairs = self.create_sample_qa_pairs()
        
        with open(os.path.join(self.data_dir, 'scraped_content.json'), 'w', encoding='utf-8') as f:
            json.dump(demo_content, f, indent=2, ensure_ascii=False)
        
        with open(os.path.join(self.data_dir, 'sample_qa_pairs.json'), 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
        
        print(f"Demo data saved to {self.data_dir}")
        print(f"- Created {len(demo_content)} demo pages")
        print(f"- Created {len(qa_pairs)} sample Q&A pairs")

if __name__ == "__main__":
    creator = DemoDataCreator()
    creator.save_demo_data()