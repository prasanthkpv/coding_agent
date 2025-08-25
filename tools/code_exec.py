import subprocess
import re

def run_code(code: str) -> str:
    try:
        proc = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        return proc
    except Exception as e:
        return f"Error running code: {e}"


def extract_code(text: str) -> str:
    """
    Extract Python code blocks from AI response.
    Falls back to returning original text if no block found.
    """
    # Match ```python ... ``` or ``` ... ```
    matches = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if matches:
        return "\n\n".join(matches).strip()
    return text.strip()
