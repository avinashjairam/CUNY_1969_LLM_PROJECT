import streamlit as st
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from chatbot_simple import SimpleCUNY1969Chatbot
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(
    page_title="CUNY 1969 Historical Chatbot",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for 25px fonts
st.markdown("""
<style>
    /* Main content fonts */
    .stChatMessage {
        font-size: 25px !important;
    }
    .stMarkdown {
        font-size: 25px !important;
    }
    .stChatMessage .stMarkdown {
        font-size: 25px !important;
    }
    .stButton > button {
        font-size: 25px !important;
        padding: 12px 20px !important;
    }
    .stTextInput > div > div > input {
        font-size: 25px !important;
    }
    .stTextArea > div > div > textarea {
        font-size: 25px !important;
    }
    
    /* Headers */
    h1 {
        font-size: 40px !important;
    }
    h2 {
        font-size: 32px !important;
    }
    h3 {
        font-size: 28px !important;
    }
    
    /* Sidebar */
    .stSidebar .stMarkdown {
        font-size: 22px !important;
    }
    .stSidebar .stButton > button {
        font-size: 20px !important;
    }
    
    /* Chat input bar - this is the key fix */
    .stChatInput > div {
        font-size: 25px !important;
    }
    .stChatInput input {
        font-size: 25px !important;
        height: 60px !important;
        padding: 15px !important;
    }
    .stChatInput textarea {
        font-size: 25px !important;
        padding: 15px !important;
    }
    
    /* Force all text elements */
    div[data-testid="stMarkdownContainer"] {
        font-size: 25px !important;
    }
    p {
        font-size: 25px !important;
    }
    
    /* Chat message containers */
    div[data-testid="chatMessage"] {
        font-size: 25px !important;
    }
    div[data-testid="chatMessage"] .stMarkdown {
        font-size: 25px !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    return SimpleCUNY1969Chatbot()

def stream_text(text):
    """Stream text with typewriter effect that simulates thinking"""
    placeholder = st.empty()
    displayed_text = ""
    
    # Show thinking indicator first
    thinking_dots = [".", "..", "...", ""]
    for i in range(8):  # Show thinking for ~2 seconds
        dots = thinking_dots[i % 4]
        placeholder.markdown(f"<div style='font-size: 25px; color: #888;'>Thinking{dots}</div>", unsafe_allow_html=True)
        time.sleep(0.25)
    
    # Now stream the actual text
    words = text.split()
    for i, word in enumerate(words):
        displayed_text += word + " "
        placeholder.markdown(f"<div style='font-size: 25px;'>{displayed_text}</div>", unsafe_allow_html=True)
        
        # Variable speed - slower for longer words, pauses at punctuation
        if word.endswith(('.', '!', '?')):
            time.sleep(0.3)  # Longer pause at end of sentences
        elif word.endswith((',', ';', ':')):
            time.sleep(0.15)  # Medium pause at punctuation
        elif len(word) > 8:
            time.sleep(0.08)  # Slower for long words
        else:
            time.sleep(0.05)  # Normal speed for short words
    
    return placeholder

def display_images(images):
    """Display images with proper handling"""
    if images:
        st.markdown("<div style='font-size: 25px; font-weight: bold;'>📸 Historical Images:</div>", unsafe_allow_html=True)
        
        cols = st.columns(min(len(images), 3))
        for idx, img_data in enumerate(images):
            with cols[idx % 3]:
                file_name = img_data.get('file', '')
                
                # Try different path strategies
                current_dir = os.path.dirname(os.path.abspath(__file__))
                possible_paths = [
                    os.path.join(current_dir, "..", "assets", file_name),
                    os.path.join(current_dir, "assets", file_name),
                    os.path.join("assets", file_name),
                    os.path.join("..", "assets", file_name)
                ]
                
                st.markdown(f"<div style='font-size: 22px;'><strong>{img_data['alt_text']}</strong></div>", unsafe_allow_html=True)
                
                image_loaded = False
                
                # Try to find and load the image
                for path in possible_paths:
                    if os.path.exists(path):
                        try:
                            # Skip the demo image
                            if "protest_demo.jpg" in path:
                                continue
                            img = Image.open(path)
                            st.image(img, caption=img_data['alt_text'], use_container_width=True)
                            st.markdown(f"<div style='font-size: 16px; color: green;'>✅ Loaded: {os.path.basename(path)}</div>", unsafe_allow_html=True)
                            image_loaded = True
                            break
                        except Exception as e:
                            st.markdown(f"<div style='font-size: 16px; color: red;'>❌ Error with {path}: {str(e)[:50]}...</div>", unsafe_allow_html=True)
                
                # If no local image found, try direct URL from CUNY site
                if not image_loaded:
                    # Try direct URL from the CUNY website
                    direct_url = img_data.get('url')
                    if direct_url:
                        try:
                            st.image(direct_url, caption=img_data['alt_text'], use_container_width=True)
                            st.markdown(f"<div style='font-size: 16px; color: green;'>🌐 Loaded from CUNY archives</div>", unsafe_allow_html=True)
                            image_loaded = True
                        except Exception as e:
                            st.markdown(f"<div style='font-size: 16px; color: orange;'>⚠️ CUNY URL failed: {str(e)[:30]}...</div>", unsafe_allow_html=True)
                    
                    # If CUNY URL also failed, use placeholder
                    if not image_loaded:
                        try:
                            # Different placeholder for each image type
                            if "protest" in file_name or "demonstration" in file_name:
                                placeholder_url = "https://via.placeholder.com/400x300/4a90e2/ffffff?text=Student+Protest+Photo"
                            elif "demands" in file_name:
                                placeholder_url = "https://via.placeholder.com/400x300/e24a4a/ffffff?text=Five+Demands+Poster"
                            elif "clash" in file_name or "police" in file_name:
                                placeholder_url = "https://via.placeholder.com/400x300/ff6b35/ffffff?text=Police+Clash+Photo"
                            elif "harlem" in file_name:
                                placeholder_url = "https://via.placeholder.com/400x300/50c878/ffffff?text=University+of+Harlem"
                            else:
                                placeholder_url = "https://via.placeholder.com/400x300/cccccc/333333?text=Historical+Photo"
                            
                            st.image(placeholder_url, caption=img_data['alt_text'], use_container_width=True)
                            st.markdown(f"<div style='font-size: 16px; color: blue;'>🔗 Using placeholder image</div>", unsafe_allow_html=True)
                        except Exception as e:
                            # Ultimate fallback
                            st.info(f"📷 {img_data['alt_text']}")
                            st.markdown(f"<div style='font-size: 16px; color: red;'>❌ All image loading failed</div>", unsafe_allow_html=True)

def main():
    st.title("🏛️ CUNY 1969 Historical Chatbot")
    st.markdown("""
    Welcome to the CUNY 1969 Historical Chatbot! This demo explores the historic student protests 
    at the City University of New York that transformed higher education access.
    """)
    
    chatbot = initialize_chatbot()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
    
    # Sidebar with demo questions
    with st.sidebar:
        st.header("📋 Demo Questions")
        st.markdown("Click any question below to try it:")
        
        demo_questions = chatbot.get_demo_questions()
        for question in demo_questions:
            if st.button(question, key=f"demo_{question}"):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": question})
                
                # Add placeholder for assistant response
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "",
                    "sources": [],
                    "images": [],
                    "streaming": True
                })
                st.rerun()
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        st.info("""
        **About this Demo:**
        - Simplified version without ML dependencies
        - Pre-loaded historical content
        - Works with Python 3.13
        """)
    
    # Display chat history
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f"<div style='font-size: 25px;'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                # Assistant message
                if message.get("streaming") and not message.get("content"):
                    # This is a new streaming message, get response and stream it
                    user_question = st.session_state.messages[idx-1]["content"] if idx > 0 else ""
                    if user_question:
                        # Show initial processing message
                        processing_placeholder = st.empty()
                        processing_placeholder.markdown(f"<div style='font-size: 25px; color: #666;'>🔍 Searching CUNY 1969 archives...</div>", unsafe_allow_html=True)
                        time.sleep(1.0)  # Simulate search time
                        
                        processing_placeholder.markdown(f"<div style='font-size: 25px; color: #666;'>📚 Analyzing historical documents...</div>", unsafe_allow_html=True)
                        time.sleep(0.8)  # Simulate analysis time
                        
                        # Get the actual response
                        response = chatbot.chat(user_question)
                        
                        # Clear processing message and stream the response
                        processing_placeholder.empty()
                        stream_text(response['answer'])
                        
                        # Update the message with full content
                        st.session_state.messages[idx] = {
                            "role": "assistant",
                            "content": response['answer'],
                            "sources": response.get('sources', []),
                            "images": response.get('images', []),
                            "streaming": False
                        }
                        
                        # Display images and sources after streaming
                        if response.get('images'):
                            display_images(response['images'])
                        
                        if response.get('sources'):
                            with st.expander("📚 View Sources"):
                                for source in response['sources']:
                                    st.write(f"- {source}")
                        
                        st.rerun()
                else:
                    # Regular message display
                    st.markdown(f"<div style='font-size: 25px;'>{message['content']}</div>", unsafe_allow_html=True)
                    
                    if message.get("images"):
                        display_images(message["images"])
                    
                    if message.get("sources"):
                        with st.expander("📚 View Sources"):
                            for source in message["sources"]:
                                st.write(f"- {source}")
    
    # Welcome message
    if st.session_state.first_visit:
        with st.chat_message("assistant"):
            st.markdown("""
            <div style='font-size: 25px;'>
            Hello! I'm here to help you learn about the 1969 CUNY student protests. 
            You can ask me about what happened, key figures like Khadija DeLoache, 
            the Five Demands, or request to see historical photos. 
            <br><br>
            Try clicking one of the demo questions in the sidebar to get started!
            </div>
            """, unsafe_allow_html=True)
        st.session_state.first_visit = False
    
    # Chat input
    if prompt := st.chat_input("Ask about CUNY 1969..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Add placeholder for streaming assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": "",
            "sources": [],
            "images": [],
            "streaming": True
        })
        
        st.rerun()

if __name__ == "__main__":
    main()