import streamlit as st
import json
from dotenv import load_dotenv
from tools import summarize_pdf
from agent import generate_quiz

load_dotenv()

st.set_page_config(page_title="Summarizer", layout="centered")

st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(to bottom right, #f0f2f6, #e6e9ed); /* Subtle light grey gradient background */
}

.main > div {
    background-color: #ffffff; /* White content background */
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.05);
    border: 1px solid #e0e0e0;
}

h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a; /* Dark grey for text */
}

p, li, .st-emotion-cache-16idsys p {
    color: #4a4a4a; /* Medium grey for body text */
}

[data-testid="stFileUploader"] {
    border: 2px dashed #9C27B0; /* Purple dashed border */
    background-color: rgba(156, 39, 176, 0.05); /* Very light purple background */
    border-radius: 0.5rem;
    padding: 1rem;
}

[data-testid="stFileUploader"] label {
    color: #7B1FA2; /* Darker purple for label */
}

.stButton>button {
    color: #ffffff;
    background: linear-gradient(to right, #7B1FA2, #9C27B0); /* Purple gradient for buttons */
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.stButton>button:hover {
    background: linear-gradient(to right, #6A1B9A, #8E24AA); /* Darker purple gradient on hover */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    transform: translateY(-1px);
}

[data-testid="stRadio"] label {
    color: #4a4a4a !important; /* Make sure radio labels are visible */
}

[data-testid="stInfo"] {
    background-color: rgba(123, 31, 162, 0.1); /* Purple based info background */
    border-left: 5px solid #7B1FA2; /* Purple info border */
    color: #1a1a1a;
}

[data-testid="stSuccess"] {
    background-color: rgba(45, 156, 89, 0.1); /* Keep green for success */
    border-left: 5px solid #2d9c59;
    color: #1a1a1a;
}

[data-testid="stError"] {
    background-color: rgba(217, 48, 37, 0.1); /* Keep red for error */
    border-left: 5px solid #d93025;
    color: #1a1a1a;
}
</style>
    """, unsafe_allow_html=True)

st.title("📄 PDF Summarizer & Quiz Generator")

# Initialize session state variables
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

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

            if st.button("Create Quiz"):
                with st.spinner("Generating quiz..."):
                    quiz_json_string = generate_quiz(summary)
                    try:
                        # Clean the string in case the model returns markdown with json
                        if quiz_json_string.startswith("```json"):
                            quiz_json_string = quiz_json_string[7:-4]
                        quiz_data = json.loads(quiz_json_string)
                        st.session_state.quiz_data = quiz_data['questions']
                        st.session_state.user_answers = {i: None for i in range(len(st.session_state.quiz_data))}
                        st.session_state.quiz_submitted = False
                        st.success("Quiz Generated!")
                    except (json.JSONDecodeError, KeyError) as e:
                        st.error(f"Failed to generate a valid quiz. The model returned:\n\n{quiz_json_string}")

if st.session_state.quiz_data and not st.session_state.quiz_submitted:
    with st.form(key='quiz_form'):
        for i, q in enumerate(st.session_state.quiz_data):
            st.write(f"**Question {i+1}:** {q['question']}")
            st.session_state.user_answers[i] = st.radio(
                "Choose your answer:",
                options=q['options'],
                key=f"q_{i}",
                label_visibility="collapsed"
            )
            st.write("---")

        submit_button = st.form_submit_button(label='Submit Answers')

        if submit_button:
            st.session_state.quiz_submitted = True
            st.rerun() # Rerun to display the results

if st.session_state.quiz_submitted:
    score = 0
    for i, q in enumerate(st.session_state.quiz_data):
        if st.session_state.user_answers[i] == q['correct_answer']:
            score += 1

    st.subheader(f"Quiz Results: You scored {score}/{len(st.session_state.quiz_data)}!")

    for i, q in enumerate(st.session_state.quiz_data):
        st.write(f"**Question {i+1}:** {q['question']}")
        st.write(f"Your answer: {st.session_state.user_answers[i]}")
        st.write(f"Correct answer: {q['correct_answer']}")
        if st.session_state.user_answers[i] == q['correct_answer']:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect!")
        st.write("---")
