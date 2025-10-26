import re
from typing import Dict
from backend.llm_utils import llm
from backend.parsing_utils import extract_json_from_llm_output


def test_engineer(state: Dict) -> Dict:
    """
    Test Engineer Agent
    -------------------
    Generates pytest-compatible unit test files for the given project code.
    """
    current_files = state.get("files", {})
    design_plan = state["design_plan"]

    # Format code files for context
    code_summary = "\n".join(
        [f"--- File: {name} ---\n{content}" for name, content in current_files.items()]
    )

    prompt = f"""
    You are an expert QA/Test Engineer.

    Your task is to write high-quality unit tests using **pytest** for the following project code,
    following the project's Design Plan.

    Design Plan:
    {design_plan}

    Current Application Files (to be tested):
    {code_summary}

    CRITICAL 1: **Strictly adhere to the file names for tests suggested in the Design Plan.**
    CRITICAL 2: **ONLY include `tests/__init__.py` or
        any other `__init__.py` files IF they are strictly required**.
        If you include them, they must be completely empty.
    CRITICAL 3: Output your response as a single valid JSON object wrapped in markdown fences, like:

    ```json
    {{
        "tests/test_main.py": "import pytest; from app.main import ...",
        "tests/__init__.py": ""
    }}
    ```

    Do not include any text or explanation outside the JSON block.
    """

    result = llm.invoke(prompt)

    # Extract JSON structure
    generated_test_files = extract_json_from_llm_output(
        result.content, "Failed to parse test files from Test Engineer Agent."
    )

    # --- Post-Processing Cleanup for filenames and __init__.py ---
    cleaned_test_files = {}
    for fname, content in generated_test_files.items():
        new_fname = fname.strip()

        # Normalize ANY variant of init.py (handles spaces, mixed slashes, or casing)
        new_fname = re.sub(
            r"([\\/])\s*init\s*\.py\s*$",
            r"\1__init__.py",
            new_fname,
            flags=re.IGNORECASE,
        )

        # Ensure __init__.py files are always empty
        if new_fname.endswith("__init__.py"):
            cleaned_test_files[new_fname] = ""
        else:
            cleaned_test_files[new_fname] = (content or "").strip()

    # Merge test files with existing app files
    final_files = {**current_files, **cleaned_test_files}

    # Remove invalid/empty keys
    final_files = {k: v for k, v in final_files.items() if k.strip() and v is not None}

    return {"files": final_files, "prompt": state.get("prompt", "")}
