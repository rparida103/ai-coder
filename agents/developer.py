import re
from typing import Dict
from backend.llm_utils import llm
from backend.parsing_utils import extract_json_from_llm_output


def developer(state: Dict) -> Dict:
    """
    Developer Agent
    ----------------
    Generates Python project files based on the design plan.
    Each file should be modular, valid Python code following the given structure.
    """
    prompt = f"""
    You are a senior Python software engineer in an autonomous AI dev team.
    Based on the following Design Plan, generate all necessary Python source files
    for the project. Each file should be a valid Python module, and filenames should
    follow the structure described in the Design Plan.

    Design Plan:
    {state['design_plan']}

    CRITICAL 1: Output your response as a single valid JSON object wrapped in markdown fences, like:
    ```json
    {{
        "app/main.py": "def handler(): ...",
        "app/utils/helpers.py": "def helper(): ...",
        "app/__init__.py": ""
    }}
    ```
    CRITICAL 2: If the Design Plan mentions package directories (e.g. `app/`),
    include an `__init__.py` file in each package folder.
    These `__init__.py` files must be completely empty.
    CRITICAL 3: Maintain the directory hierarchy as described in the Design Plan.
    CRITICAL 4: Include a non-empty `requirements.txt` file,
        listing ALL external Python dependencies that your generated code uses.
        - This file must contain at least one package if your code imports anything external
        (e.g., streamlit, flask, requests, pandas, fastapi, etc.).
        - If your code uses only Python's standard library, include a comment line saying -
        "# No external dependencies required".
    CRITICAL 5: Do not merge multiple files into one — every module must be its own file.
    CRITICAL 6: Do not include explanations or markdown outside the JSON block.
    CRITICAL 7: Do not include empty placeholder files.
        If a file is part of the design but has no logic, omit it completely.
    """

    result = llm.invoke(prompt)

    # Extract JSON structure from LLM output
    generated_files = extract_json_from_llm_output(
        result.content, "Failed to parse files from Developer Agent."
    )

    # --- Post-Processing Cleanup for filenames and __init__.py ---
    cleaned_files = {}
    for fname, content in generated_files.items():
        new_fname = fname.strip()

        # Normalize ANY variant of init.py (handles spaces, mixed slashes, or casing)
        # e.g. calculator_app/ui/init.py -> calculator_app/ui/__init__.py
        new_fname = re.sub(
            r"([\\/])\s*init\s*\.py\s*$",
            r"\1__init__.py",
            new_fname,
            flags=re.IGNORECASE,
        )

        # Ensure __init__.py files are empty
        if new_fname.endswith("__init__.py"):
            cleaned_files[new_fname] = ""
        else:
            cleaned_files[new_fname] = (content or "").strip()

    # Remove invalid/empty entries
    cleaned_files = {
        k: v for k, v in cleaned_files.items() if k.strip() and v is not None
    }

    # Merge with existing files in state
    existing_files = state.get("files", {})
    final_files = {**existing_files, **cleaned_files}

    return {"files": final_files, "prompt": state.get("prompt", "")}
