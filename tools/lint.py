def lint_code(code: str) -> str:
    if "print(" not in code:
        return "Warning: No print statement found."
    return "Code looks fine!"
