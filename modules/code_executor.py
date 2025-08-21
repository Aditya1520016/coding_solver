# modules/code_executor.py
import subprocess
import sys
from typing import List, Dict


__all__ = ["run_on_examples"]




def run_on_examples(solution_file: str, examples: List[Dict[str, str]], timeout_sec: int = 10):
	"""Run the generated solution against parsed examples.
	Each example is a dict with keys: 'input', 'output'.
	Returns a list of dicts with pass/fail and outputs.
	"""
	results = []
	for idx, ex in enumerate(examples, start=1):
		proc = subprocess.run(
			[sys.executable, solution_file],
			input=(ex.get("input", "")).encode("utf-8"),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			timeout=timeout_sec,
		)
		got = proc.stdout.decode("utf-8").strip()
		expected = (ex.get("output", "")).strip()
		results.append({
			"example": idx,
			"input": ex.get("input", "").strip(),
			"expected": expected,
			"got": got,
			"pass": (got == expected),
			"stderr": proc.stderr.decode("utf-8").strip(),
			"returncode": proc.returncode,
		})
	return results