import json
import re

# ============================================================
# SAFE JSON
# ============================================================

def safe_json(text):

    if text is None:
        raise ValueError("GPT returned None")

    text = text.strip()

    if len(text) == 0:
        raise ValueError("GPT returned empty response")

    try:
        return json.loads(text)

    except Exception:
        pass

    match = re.search(
        r"\{[\s\S]*\}",
        text
    )

    if match:

        candidate = match.group(0)

        try:
            return json.loads(candidate)

        except Exception:
            pass

    print("\n================ GPT RAW OUTPUT ================\n")
    print(text)
    print("\n================================================\n")

    raise ValueError("Invalid JSON")