import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def call_gemini_for_summary(text):
    prompt = f"""
    Please act as an expert summarizer. Your task is to provide a high-quality summary of the following text extracted from a PDF.
    The summary should be:
    1.  **Concise and Clear**: Capture the main ideas and key points without unnecessary jargon.
    2.  **Well-structured**: Use bullet points or numbered lists to highlight the most important information.
    3.  **Easy to Understand**: Write in simple, clear language that a student can easily comprehend.
    4.  **Comprehensive**: Do not leave out critical information.

    Here is the text to summarize:
    ---
    {text}
    ---
    """
    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are an expert summarizer that produces clear, well-structured summaries for students."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

def generate_quiz(summary):
    prompt = f"""
    Based on the following summary, create a JSON object for a quiz with 5 multiple-choice questions.
    The JSON object should have a single key "questions" which is a list of question objects.
    Each question object should have three keys:
    1. "question": The question text (string).
    2. "options": A list of 4 strings, where one is the correct answer.
    3. "correct_answer": The string of the correct answer.

    Do not include any text outside of the JSON object.

    Summary:
    ---
    {summary}
    ---
    """
    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates quizzes in JSON format."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        # The response is expected to be a JSON string.
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating quiz: {e}"
