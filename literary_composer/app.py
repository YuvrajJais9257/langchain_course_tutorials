import streamlit as st
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq 
from langchain_core.output_parsers import StrOutputParser
from constants.templates import PERSONA_MAP, TEMPLATES
from langchain_ollama import ChatOllama

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Page Config ---
st.set_page_config(
    page_title="AI Literary Composer", 
    page_icon="✍️",
    layout="wide"
)

# Initialize session state to store the result
if "generated_work" not in st.session_state:
    st.session_state.generated_work = ""

# --- Header ---
st.title("✍️ AI Literary Composer")
st.markdown("Generate masterful works by adjusting the persona and creativity dial.")

# --- Sidebar Logic ---
with st.sidebar:
    st.header("Specialist Settings")
    
    # Selection 1: The Persona
    persona = st.selectbox("Select Specialist", list(PERSONA_MAP.keys()))
    
    # Selection 2: The Literature (Dynamic based on Persona)
    literature_options = PERSONA_MAP[persona]
    literature = st.selectbox(
        "Literature Type", 
        literature_options,
        help="Choose the format"
    )
    
    temp = st.slider(
        "Creativity (Temperature)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.8,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )

    st.markdown("---")

    st.info(f"**Active Style**\n\n{persona} → {literature}")

# --- Main UI ---
theme_input = st.text_area(
    "What should it be about?", 
    placeholder="e.g., Nostalgic new year celebrations, a hero's last stand, the ethics of AI...",
    height=120
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(
        "🎨 Generate Masterpiece", 
        type="primary",
        use_container_width=True
    )

if generate_button:
    if theme_input.strip():
        with st.spinner(f"✨ The {persona} is consulting the muse..."):
            try:
                # Initialize LLM
                # llm = ChatOllama(
                #     model="gemma3",
                #     temperature=temp
                # )
                llm = ChatGroq(
                    api_key=os.getenv("GROQ_API_KEY"),
                    model="llama-3.3-70b-versatile",
                    temperature=temp
                )
                
                # Get the specific template
                selected_template = TEMPLATES[persona][literature]
                
                # Create chain
                chain = selected_template | llm | StrOutputParser()
                
                # Generate response
                response = chain.invoke({"theme": theme_input})
                
                # Store in session state
                st.session_state.generated_work = response
                
                st.success("✅ Masterpiece generated!")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a theme first!")

# Display and Download
if st.session_state.generated_work:
    st.markdown("---")
    st.subheader("📜 Your Masterpiece")
    
    # Display in a clean, professional container
    # The 'white-space: pre-wrap' is essential for keeping poem/prose formatting
    st.markdown(
        f"""
        <div style='background-color: white; color: #333; padding: 30px; 
                    border-radius: 8px; border-left: 6px solid #ff6b6b;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    font-family: "Helvetica Neue", sans-serif; font-size: 16px;
                    line-height: 1.7; white-space: pre-wrap;'>
            {st.session_state.generated_work}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Action Buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Download Button
        st.download_button(
            label="📥 Download",
            data=st.session_state.generated_work,
            file_name=f"{persona}_{literature}_{theme_input[:20].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Copy Button (Using a simple text area trick or just a clear label)
        if st.button("📋 Copy Text", use_container_width=True):
            # This doesn't auto-copy to system clipboard without JS, 
            # but providing a text area makes it easy for the user
            st.info("Select and copy the text above!")
    
    with col3:
        # Clear Button
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.generated_work = ""
            st.rerun()