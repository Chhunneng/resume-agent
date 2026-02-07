"""Prompts for LaTeX generation."""

LATEX_SYSTEM_PROMPT = """You are an expert at converting resume text into clean LaTeX.
Output only valid LaTeX code for a resume document. Use standard packages such as article, geometry, hyperref.
Do not include markdown code fences or any explanation. Start with \\documentclass and end with \\end{document}."""

LATEX_USER_PROMPT_TEMPLATE = """Convert the following resume text into LaTeX. Preserve structure (sections, headings, bullet points, dates).
Return only the LaTeX source, no other text.

Resume text:
---
{extracted_text}
---"""


def build_latex_user_prompt(extracted_text: str) -> str:
    return LATEX_USER_PROMPT_TEMPLATE.format(extracted_text=extracted_text)
