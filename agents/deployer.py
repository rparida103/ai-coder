from backend.llm_utils import llm


def deployer(state):
    prompt = f"""
    You are a DevOps engineer.
    Provide a simple deployment guide for the following code and tests.
    Code:
    {state['code']}
    Tests:
    {state['tests']}
    """
    result = llm.invoke(prompt)
    return {"deployment_guide": result.content}
