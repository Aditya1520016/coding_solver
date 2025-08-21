🧑‍💻 Coding Solver (AI-Powered Problem Solver)

An AI-powered coding assistant that helps you solve programming problems by generating step-by-step explanations and working solution code. Built with Python, Tkinter GUI, and OpenAI API, this tool makes coding easier and faster for beginners and professionals alike.

🚀 Features

🔹 AI Problem Solving – Enter a coding problem, and the AI generates an explanation and solution code.

🔹 Code Generation – Solutions are provided in clean, ready-to-run code.

🔹 GUI Interface – Simple Tkinter-based interface for easy interaction.

🔹 Copy & Save Solutions – Copy generated code directly or save it locally.

🔹 Multiple Language Support (optional) – Can be extended to Python, Java, C++, etc.

🔹 Lightweight & Easy to Use – No extra heavy setup required.

📂 Project Structure
coding_solver/
│── main.py                 # Tkinter GUI entry point
│── modules/
│   ├── ai_solver.py        # Handles AI requests & responses
│   ├── utils.py            # Helper functions
│── assets/                 # (optional) icons, images, screenshots
│── README.md               # Project documentation
│── requirements.txt        # Dependencies

🛠️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/coding_solver.git
cd coding_solver

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up OpenAI API Key

Get your API key from OpenAI

Create a .env file in the project root and add:

OPENAI_API_KEY=your_api_key_here

▶️ Usage

Run the app with:

python main.py

Example:

Open the GUI.

Enter a coding problem (e.g., “Write a function to check if a number is prime”).

Click Generate Solution.

The AI will return:

✅ Explanation of the logic.

✅ Solution code (Python by default).

Copy the solution and run it!

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a new branch (feature-new)

Commit your changes

Push and submit a Pull Request

📝 License

This project is licensed under the MIT License – you’re free to use and modify it.

⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub.
