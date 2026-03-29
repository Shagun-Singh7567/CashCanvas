from ai.client import ask

# These must match the options shown in the transaction form exactly.
CATEGORIES = [
    "Food & Dining", "Transportation", "Shopping",
    "Entertainment", "Health", "Utilities", "Education", "Other"
]

SYSTEM_PROMPT = f"""
You are a transaction categorizer for a personal finance app.
Given a short transaction description, reply with ONLY the single best matching
category from this list — nothing else, no explanation, no punctuation:

{", ".join(CATEGORIES)}

If nothing fits well, reply with: Other
""".strip()


def suggest_category(description: str) -> str:
    """
    Returns a category string for the given transaction description.
    Falls back to "Other" if the AI returns something unexpected.
    """
    if not description.strip():
        return "Other"

    result = ask(SYSTEM_PROMPT, description.strip())

    # Validate — only accept a known category
    for cat in CATEGORIES:
        if cat.lower() in result.lower():
            return cat
    return "Other"