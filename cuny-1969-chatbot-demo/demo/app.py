import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from chatbot import CUNY1969Chatbot
from demo_data import DemoDataCreator
from knowledge_base import CUNY1969KnowledgeBase
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="CUNY 1969 Historical Chatbot",
    page_icon="📚",
    layout="wide"
)

@st.cache_resource
def initialize_system():
    with st.spinner("Initializing demo data and knowledge base..."):
        creator = DemoDataCreator()
        creator.save_demo_data()
        
        kb = CUNY1969KnowledgeBase()
        kb.build_knowledge_base()
        
        chatbot = CUNY1969Chatbot()
        
    return chatbot

def display_images(images):
    if images:
        cols = st.columns(min(len(images), 3))
        for idx, img_data in enumerate(images):
            with cols[idx % 3]:
                try:
                    img_path = os.path.join("..", "assets", img_data['local_path'])
                    if os.path.exists(img_path):
                        img = Image.open(img_path)
                        st.image(img, caption=img_data['alt_text'], use_column_width=True)
                    else:
                        st.info(f"📷 {img_data['alt_text']}")
                except:
                    st.info(f"📷 {img_data['alt_text']}")

def main():
    st.title("🏛️ CUNY 1969 Historical Chatbot")
    st.markdown("""
    Welcome to the CUNY 1969 Historical Chatbot! This demo explores the historic student protests 
    at the City University of New York that transformed higher education access.
    """)
    
    chatbot = initialize_system()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
    
    with st.sidebar:
        st.header("📋 Demo Questions")
        st.markdown("Click any question below to try it:")
        
        demo_questions = chatbot.get_demo_questions()
        for question in demo_questions:
            if st.button(question, key=f"demo_{question}"):
                st.session_state.messages.append({"role": "user", "content": question})
                
                with st.spinner("Searching archives..."):
                    response = chatbot.chat(question)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response['answer'],
                    "sources": response.get('sources', []),
                    "images": response.get('images', [])
                })
                st.rerun()
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            chatbot.clear_context()
            st.rerun()
        
        st.divider()
        st.info("""
        **About this Demo:**
        - Uses local vector search
        - No external APIs required
        - Historical content from CUNY 1969 archives
        """)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            if message["role"] == "assistant":
                if message.get("images"):
                    display_images(message["images"])
                
                if message.get("sources"):
                    with st.expander("📚 View Sources"):
                        for source in message["sources"]:
                            st.write(f"- {source}")
    
    if st.session_state.first_visit:
        with st.chat_message("assistant"):
            st.write("""
            Hello! I'm here to help you learn about the 1969 CUNY student protests. 
            You can ask me about what happened, key figures like Khadija DeLoache, 
            the Five Demands, or request to see historical photos. 
            
            Try clicking one of the demo questions in the sidebar to get started!
            """)
        st.session_state.first_visit = False
    
    if prompt := st.chat_input("Ask about CUNY 1969..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Searching archives..."):
                response = chatbot.chat(prompt)
            
            st.write(response['answer'])
            
            if response.get('images'):
                display_images(response['images'])
            
            if response.get('sources'):
                with st.expander("📚 View Sources"):
                    for source in response['sources']:
                        st.write(f"- {source}")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['answer'],
                "sources": response.get('sources', []),
                "images": response.get('images', [])
            })

if __name__ == "__main__":
    main()