from backend.llm_utils import llm
from typing import Dict, Any


def architect(state: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate a high-level design plan, including component breakdown and file structure.
    """
    prompt = f"""
    You are a senior software architect.
    The project requirement is: {state['prompt']}

    Create a concise high-level design plan that includes:
    1. **Project Components:** A list of the main modules or classes.
    2. **File Structure:** A preliminary breakdown of the necessary files
    (e.g., 'main.py', 'models/__init__.py', 'requirements.txt') and
    what each file will contain.
    **Ensure correct use of special names like '__init__.py' for Python packages.**
    3. **Architecture:** High-level details on how the components interact.

    Format the response clearly using Markdown headings.
    """
    result = llm.invoke(prompt)
    return {"design_plan": result.content}
