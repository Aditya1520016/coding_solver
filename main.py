import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

from modules import ocr_module, parser_module, code_executor
from modules import ai_solver   # ✅ new module for AI-powered solving
from dotenv import load_dotenv
load_dotenv()


class CodingSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Coding Problem Solver")
        self.root.geometry("980x720")

        # Buttons (top row)
        top = tk.Frame(root)
        top.pack(pady=8)

        tk.Button(top, text="📸 Capture Screen", command=self.capture_screen, font=("Arial", 11)).grid(row=0, column=0, padx=6)
        tk.Button(top, text="🔍 Extract & Append Text", command=self.extract_text, font=("Arial", 11)).grid(row=0, column=1, padx=6)
        tk.Button(top, text="🧠 Parse Problem", command=self.parse_problem, font=("Arial", 11)).grid(row=0, column=2, padx=6)
        tk.Button(top, text="⚙️ Generate Solution", command=self.generate_solution, font=("Arial", 11)).grid(row=0, column=3, padx=6)
        tk.Button(top, text="▶️ Run & Test", command=self.run_tests, font=("Arial", 11)).grid(row=0, column=4, padx=6)

        # OCR / Problem text area
        tk.Label(root, text="Problem Text (OCR)", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=120, height=20, font=("Consolas", 10))
        self.text_area.pack(padx=10, pady=6)

        # Log area
        tk.Label(root, text="Logs & Results", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=120, height=12, font=("Consolas", 10))
        self.log_area.pack(padx=10, pady=6)

        # Paths/state
        self.screenshot_path = os.path.join("screenshots", "screenshot.png")
        self.solution_path = os.path.join("solutions", "solution.py")
        self.parsed = None

        # Ensure folders exist
        os.makedirs(os.path.dirname(self.screenshot_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.solution_path), exist_ok=True)

    # --- Capture & OCR ---
    def capture_screen(self):
        self.root.iconify()
        self.root.after(800, self._take_screenshot)

    def _take_screenshot(self):
        saved_path = ocr_module.capture_screen(self.screenshot_path)
        self.root.deiconify()
        if saved_path:
            messagebox.showinfo("Screenshot", f"Saved: {saved_path}")
            self._log(f"Screenshot captured -> {saved_path}")
        else:
            messagebox.showerror("Error", "Failed to capture screenshot")
            self._log("ERROR: Could not capture screenshot.")

    def extract_text(self):
        text = ocr_module.extract_text(self.screenshot_path)
        if not text:
            messagebox.showerror("Error", "No text extracted!")
            self._log("ERROR: OCR returned empty text.")
            return
        self.text_area.insert(tk.END, "\n" + text.strip() + "\n")
        self.text_area.see(tk.END)
        self._log("OCR text appended to editor.")

    # --- Parse, Generate, Run ---
    def parse_problem(self):
        raw = self.text_area.get("1.0", tk.END)
        if not raw.strip():
            messagebox.showerror("Error", "Problem text is empty.")
            return
        self.parsed = parser_module.parse_problem_text(raw)
        ex_count = len(self.parsed.get("examples", []))
        self._log(f"Parsed title: {self.parsed.get('title', '')}")
        self._log(f"Found {ex_count} example(s).")
        if ex_count == 0:
            self._log("No examples detected. You can still generate a solution.")
        messagebox.showinfo("Parsed", f"Parsing complete. Examples found: {ex_count}")

    def generate_solution(self):
        if not self.parsed:
            messagebox.showerror("Error", "Parse the problem first.")
            self._log("ERROR: Generate requested without parsed problem.")
            return

        # ✅ NEW: Call AI model
        problem_text = self.text_area.get("1.0", tk.END).strip()
        solution_code = ai_solver.solve_with_ai(problem_text)

        if not solution_code or "ERROR" in solution_code:
            messagebox.showerror("Error", "AI failed to generate solution.")
            self._log(solution_code)
            return

        with open(self.solution_path, "w", encoding="utf-8") as f:
            f.write(solution_code)

        self._log("✅ AI-generated solution written to solution.py")
        messagebox.showinfo("Solution", "AI-generated solution created!")

    def run_tests(self):
        if not os.path.exists(self.solution_path):
            messagebox.showerror("Error", "No solution file found. Generate it first.")
            self._log("ERROR: Run requested but solution.py not found.")
            return
        examples = self.parsed.get("examples", []) if self.parsed else []
        if not examples:
            self._log("No examples available. Running with the entire OCR text as input.")
            examples = [{"input": self.text_area.get("1.0", tk.END), "output": ""}]
        results = code_executor.run_on_examples(self.solution_path, examples)
        for r in results:
            mark = "✅ PASS" if r["pass"] else "❌ FAIL"
            self._log(f"Example {r['example']}: {mark}\n  input: {r['input']}\n  expected: {r['expected']}\n  got: {r['got']}")
            if r["stderr"]:
                self._log(f"  stderr: {r['stderr']}")

    # --- Utils ---
    def _log(self, msg: str):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodingSolverApp(root)
    root.mainloop()
