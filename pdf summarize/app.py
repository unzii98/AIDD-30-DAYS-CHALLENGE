import streamlit as st
from dotenv import load_dotenv
from tools import summarize_pdf
from agent import generate_quiz

from agent import call_gemini_for_summary, generate_quiz



load_dotenv()



st.set_page_config(page_title="PDF Summarizer", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Orbitron', sans-serif;
    background: #000;
}

[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/2150/sky-space-dark-galaxy.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.main > div {
    background-color: rgba(10, 0, 30, 0.5); /* Deep purple transparent bg */
    padding: 2rem;
    border-radius: 1rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 0, 255, 0.3); /* Neon pink border */
}

h1 {
    color: #ff00ff; /* Neon Pink */
    text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff; /* Reduced blur */
}

h2, h3, h4, h5, h6 {
    color: #00ffff; /* Neon Cyan */
    text-shadow: 0 0 3px #00ffff, 0 0 5px #00ffff;
}

p, li, .st-emotion-cache-16idsys p {
    color: #f0f0f0; /* Lighter text for readability */
}

[data-testid="stFileUploader"] {
    border: 2px dashed #ff00ff;
    background-color: rgba(255, 0, 255, 0.1);
    border-radius: 0.5rem;
    padding: 1rem;
}

[data-testid="stFileUploader"] label {
    color: #ff00ff;
    text-shadow: 0 0 3px #ff00ff;
}

.stButton>button {
    color: #000;
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px #ff00ff, 0 0 25px #00ffff;
}

.stButton>button:hover {
    box-shadow: 0 0 25px #ff00ff, 0 0 40px #00ffff;
    transform: scale(1.05);
}

.stProgress > div > div > div > div {
    background: linear-gradient(45deg, #00ffff, #ff00ff);
}

[data-testid="stInfo"] {
    background-color: rgba(0, 255, 255, 0.1);
    border-left: 5px solid #00ffff;
    color: #f0f0f0;
}

[data-testid="stSuccess"] {
    background-color: rgba(0, 255, 127, 0.1);
    border-left: 5px solid #00ff7f;
    color: #f0f0f0;
}

[data-testid="stError"] {
    background-color: rgba(255, 71, 87, 0.1);
    border-left: 5px solid #ff4757;
    color: #f0f0f0;
}

footer {
    visibility: hidden;
}

/* New additions to hide more potential "boxes" */
[data-testid="stToolbar"] { /* Hides the top-right menu/settings */
    display: none !important;
}

[data-testid="stStatusWidget"] { /* Hides status messages at the bottom, e.g., "Running..." */
    display: none !important;
}

.st-emotion-cache-nahz7x { /* A common class for Streamlit's top-right toolbar */
    display: none !important;
}

.st-emotion-cache-1na6f7v { /* A common class for the "Made with Streamlit" footer text */
    display: none !important;
}

#MainMenu { /* Hides the hamburger menu */
    visibility: hidden;
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 PDF Summarizer & Quiz Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")

    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

        st.info("Summarizing your PDF... Please wait ⚙️")
        summary = summarize_pdf("uploaded.pdf")
    
        if summary.startswith("Error") or summary.startswith("Could not extract") or summary.startswith("An unexpected error"):
            st.error(summary)
        else:
            st.subheader("📌 Summary")
            st.write(summary)
    
            st.subheader("📝 Generate Quiz")
            @st.cache_data
            def generate_quiz_cached(summary):
                with st.spinner("Generating quiz..."):
                    return generate_quiz(summary)
    
            if st.button("Create Quiz"):
                quiz = generate_quiz_cached(summary)
                if quiz.startswith("An error occurred"):
                    st.error(quiz)
                else:
                    st.success("Quiz Generated!")
                    st.write(quiz)
