# modules/parser_module.py
import re
from typing import Dict, List


__all__ = ["parse_problem_text"]


CLEAN_MAP = {
"—": "-",
"–": "-",
"’": "'",
"‘": "'",
"“": '"',
"”": '"',
}


UI_NOISE_PATTERNS = [
r"\bDescription\b.*?\bCode\b",
r"\bSolutions\b",
r"\bSubmissions\b",
r"\bPremium\b",
r"\bHint\b",
r"\bTopics?\b.*?\bCompanies\b",
]


def _clean(text: str) -> str:
	if not text:
		return ""
	for k, v in CLEAN_MAP.items():
		text = text.replace(k, v)
	# normalize spaces
	text = text.replace("\r", "")
	text = re.sub(r"[\t\x0b\x0c]+", " ", text)
	text = re.sub(r"\u200b", "", text) # zero-width space
	# strip obvious UI noise chunks
	for pat in UI_NOISE_PATTERNS:
		text = re.sub(pat, " ", text, flags=re.IGNORECASE | re.DOTALL)
	# collapse whitespace
	text = re.sub(r"\s+", " ", text)
	return text.strip()




def parse_problem_text(raw_text: str) -> Dict:
	"""Parse OCR text into a structured dict: title, description, examples.
	Returns: { 'title': str, 'description': str, 'examples': List[{'input':str,'output':str}] }
	"""
	t = _clean(raw_text)

	# Heuristic title: first 12-15 words or sentence up to first example/input
	title_end = re.search(r"(Example\s*1|Examples?:|Input\s*:)", t, re.IGNORECASE)
	title_block = t[: title_end.start()] if title_end else t
	# Try to grab first sentence-like span
	m = re.search(r"([A-Z].{10,120}?[.!?])", title_block)
	title = (m.group(1) if m else title_block[:120]).strip()

	# Description = up to first Example/Input
	desc_end = re.search(r"(Example\s*1|Examples?:|Input\s*:)", t, re.IGNORECASE)
	description = t[: desc_end.start()].strip() if desc_end else t

	# Examples: support both "Example 1:" blocks and loose Input/Output pairs
	examples: List[Dict[str, str]] = []

	# Split by examples and scan blocks
	blocks = re.split(r"Example\s*\d+\s*:?", t, flags=re.IGNORECASE)
	for blk in blocks[1:]:
		mi = re.search(r"Input\s*:?\s*(.+?)\s*Output\s*:?\s*([^\n]+)", blk, re.IGNORECASE | re.DOTALL)
		if mi:
			inp = mi.group(1).strip()
			outp = mi.group(2).strip()
			outp = re.split(r"Explanation", outp, flags=re.IGNORECASE)[0].strip()
			examples.append({"input": inp, "output": outp})

	if not examples:
		for mi in re.finditer(r"Input\s*:?\s*(.+?)\s*Output\s*:?\s*([^\n]+)", t, re.IGNORECASE | re.DOTALL):
			inp = mi.group(1).strip()
			outp = re.split(r"Explanation", mi.group(2), flags=re.IGNORECASE)[0].strip()
			examples.append({"input": inp, "output": outp})

	return {
		"title": title,
		"description": description,
		"examples": examples,
	}