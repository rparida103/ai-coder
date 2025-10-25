from backend.llm_utils import llm


def test_engineer(state):
    prompt = f"""
    You are a QA/test engineer.
    Given this code, write unit tests using pytest.
    Code:
    {state['code']}
    """
    result = llm.invoke(prompt)
    return {"tests": result.content}
