from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.dev_lead import development_lead
from agents.developer import developer
from agents.test_engineer import test_engineer
from agents.deployer import deployer


class DevState(TypedDict):
    prompt: str
    design_plan: str
    code: str
    tests: str
    deployment_guide: str


def build_graph():
    graph = StateGraph(DevState)

    graph.add_node("development_lead", development_lead)
    graph.add_node("developer", developer)
    graph.add_node("test_engineer", test_engineer)
    graph.add_node("deployer", deployer)

    graph.set_entry_point("development_lead")
    graph.add_edge("development_lead", "developer")
    graph.add_edge("developer", "test_engineer")
    graph.add_edge("test_engineer", "deployer")
    graph.add_edge("deployer", END)

    return graph.compile()
