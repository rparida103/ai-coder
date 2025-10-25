from backend.llm_utils import llm


def developer(state):
    prompt = f"""
    You are a Python developer.
    Based on this design plan, implement the code in Python:
    {state['design_plan']}
    """
    result = llm.invoke(prompt)
    return {"code": result.content}
