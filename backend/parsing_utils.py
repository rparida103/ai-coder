import json
import re
from typing import Dict


def extract_json_from_llm_output(raw_output: str, error_msg: str) -> Dict[str, str]:
    """
    Extract and parse JSON content from LLM output.
    Handles markdown fences and malformed backslashes.
    """

    # Match JSON wrapped in ```json ... ``` or ``` ... ```
    match = re.search(r"```(json)?\s*(\{[\s\S]*?\})\s*```", raw_output, re.IGNORECASE)
    json_str = match.group(2) if match else raw_output.strip()

    if not json_str:
        raise ValueError(f"No JSON found in LLM output. {error_msg}")

    try:
        parsed_json = json.loads(json_str)
    except json.JSONDecodeError:
        # Attempt to fix malformed escape sequences
        cleaned_str = json_str.replace("\\", "\\\\").replace("\\\\\\\\", "\\\\")
        try:
            parsed_json = json.loads(cleaned_str)
        except json.JSONDecodeError as e:
            snippet = json_str[:500]
            raise ValueError(
                f"Failed to parse JSON: {error_msg}. Snippet: {snippet}"
            ) from e

    if not (
        isinstance(parsed_json, dict)
        and all(
            isinstance(k, str) and isinstance(v, str) for k, v in parsed_json.items()
        )
    ):
        raise ValueError("Parsed JSON is not a {str: str} mapping.")

    return parsed_json
