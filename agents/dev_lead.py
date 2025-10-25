from backend.llm_utils import llm

def development_lead(state):
    prompt = f"""
    You are a senior software architect.
    The project requirement is: {state['prompt']}
    Create a concise high-level design plan with components and structure.
    """
    result = llm.invoke(prompt)
    return {"design_plan": result.content}