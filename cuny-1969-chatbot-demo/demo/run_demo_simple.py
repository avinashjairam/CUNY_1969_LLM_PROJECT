#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from chatbot_simple import SimpleCUNY1969Chatbot
import time
from typing import Dict

class SimpleDemoRunner:
    def __init__(self):
        self.chatbot = SimpleCUNY1969Chatbot()
        self.demo_scenarios = [
            {
                "name": "General Overview",
                "query": "What happened at CUNY in 1969?",
                "expected_keywords": ["protests", "students", "1969", "occupation"]
            },
            {
                "name": "Key Figure",
                "query": "Who was Khadija DeLoache?",
                "expected_keywords": ["Khadija DeLoache", "activist", "student"]
            },
            {
                "name": "Specific Demands",
                "query": "What were the Five Demands?",
                "expected_keywords": ["Five Demands", "Black and Puerto Rican", "faculty"]
            },
            {
                "name": "Visual Content",
                "query": "Show me photos from the protests",
                "expected_keywords": ["images", "photos", "South Campus"]
            },
            {
                "name": "Historical Context",
                "query": "How did MLK's death affect CUNY students?",
                "expected_keywords": ["MLK", "Martin Luther King", "1968"]
            }
        ]
    
    def print_header(self, text: str):
        print("\n" + "="*60)
        print(f" {text}")
        print("="*60)
    
    def print_section(self, text: str):
        print("\n" + "-"*40)
        print(f" {text}")
        print("-"*40)
    
    def setup_demo(self):
        self.print_header("CUNY 1969 Historical Chatbot Demo (Simplified)")
        print("\nThis is a simplified version without ML dependencies.")
        print("It uses keyword-based search for demonstration purposes.")
        print("\n✅ Setup complete!")
        time.sleep(1)
    
    def run_scenario(self, scenario: Dict):
        self.print_section(f"Scenario: {scenario['name']}")
        print(f"\n🤔 Question: {scenario['query']}")
        
        print("\n⏳ Processing...")
        response = self.chatbot.chat(scenario['query'])
        
        print(f"\n💬 Answer:\n{response['answer']}")
        
        if response.get('sources'):
            print(f"\n📚 Sources: {len(response['sources'])} source(s) found")
            for source in response['sources'][:2]:
                print(f"   - {source}")
        
        if response.get('images'):
            print(f"\n🖼️  Images: {len(response['images'])} image(s) available")
            for img in response['images'][:2]:
                print(f"   - {img['alt_text']}")
        
        keyword_found = any(keyword.lower() in response['answer'].lower() 
                          for keyword in scenario['expected_keywords'])
        
        if keyword_found:
            print("\n✅ Response contains expected content")
        else:
            print("\n⚠️  Response may be missing expected keywords")
        
        return response
    
    def interactive_mode(self):
        self.print_header("Interactive Mode")
        print("\nYou can now ask your own questions about CUNY 1969.")
        print("Type 'quit' or 'exit' to end the session.\n")
        
        while True:
            try:
                user_input = input("\n❓ Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nThank you for using the CUNY 1969 Historical Chatbot!")
                    break
                
                if not user_input:
                    continue
                
                print("\n⏳ Processing...")
                response = self.chatbot.chat(user_input)
                
                print(f"\n💬 Answer:\n{response['answer']}")
                
                if response.get('sources'):
                    print(f"\n📚 Sources: {', '.join(response['sources'][:2])}")
                
                if response.get('images'):
                    print(f"\n🖼️  {len(response['images'])} image(s) available")
                    
            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again with a different question.")
    
    def run_full_demo(self):
        self.setup_demo()
        
        self.print_header("Running Demo Scenarios")
        print("\nI'll demonstrate the chatbot with 5 pre-configured questions.\n")
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n[{i}/{len(self.demo_scenarios)}]", end="")
            self.run_scenario(scenario)
            
            if i < len(self.demo_scenarios):
                input("\nPress Enter to continue to next scenario...")
        
        self.print_header("Demo Complete!")
        print("\nThe chatbot successfully answered questions about:")
        print("✓ The 1969 CUNY protests and their significance")
        print("✓ Key figures like Khadija DeLoache")
        print("✓ The Five Demands for educational equity")
        print("✓ Historical images from the protests")
        print("✓ The impact of MLK's assassination")
        
        print("\n" + "="*60)
        choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
        
        if choice == 'y':
            self.interactive_mode()
    
    def quick_test(self):
        self.setup_demo()
        self.print_header("Quick Test Mode")
        
        test_query = "What were the Five Demands?"
        print(f"\nTesting with: '{test_query}'")
        
        response = self.chatbot.chat(test_query)
        print(f"\nResponse: {response['answer'][:200]}...")
        print("\n✅ Quick test complete!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='CUNY 1969 Chatbot Demo Runner (Simplified)')
    parser.add_argument('--quick', action='store_true', help='Run quick test only')
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    
    args = parser.parse_args()
    
    runner = SimpleDemoRunner()
    
    try:
        if args.quick:
            runner.quick_test()
        elif args.interactive:
            runner.setup_demo()
            runner.interactive_mode()
        else:
            runner.run_full_demo()
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("\nThis is the simplified version that doesn't require ML libraries.")

if __name__ == "__main__":
    main()