# modules/ai_solver.py
from dotenv import load_dotenv
from openai import OpenAI
import os

# Initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def solve_with_ai(problem_text: str) -> str:
    """
    Sends the problem text to the AI model and gets back a solution code.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # use GPT-4 or GPT-4o-mini depending on access
            messages=[
                {"role": "system", "content": "You are an AI that solves coding problems. Always return only working code."},
                {"role": "user", "content": f"Solve this problem and provide only the Python solution code:\n\n{problem_text}"}
            ],
            temperature=0  # deterministic, no randomness
        )

        # Extract text
        solution_code = response.choices[0].message.content.strip()
        return solution_code

    except Exception as e:
        return f"Error while generating solution: {str(e)}"
