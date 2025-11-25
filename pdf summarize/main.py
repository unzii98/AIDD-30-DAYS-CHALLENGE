import sys
from dotenv import load_dotenv
from tools import summarize_pdf
from agent import generate_quiz

load_dotenv()

def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print("Summarizing your PDF... Please wait ⚙️")
        
        summary = summarize_pdf(pdf_path)
        
        if summary.startswith("Error") or summary.startswith("Could not extract") or summary.startswith("An unexpected error"):
            print(f"Error: {summary}")
            return

        print("📌 Summary")
        print(summary)
        
        print("\n📝 Generating Quiz...")
        quiz = generate_quiz(summary)
        
        if quiz.startswith("An error occurred"):
            print(f"Error: {quiz}")
            return
            
        print("Quiz Generated!")
        print(quiz)
    else:
        print("Usage: python main.py <path_to_pdf_file>")

if __name__ == "__main__":
    main()
