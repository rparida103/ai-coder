from backend.graph_builder import build_graph


def run_pipeline(user_prompt: str):
    graph = build_graph()
    initial_state = {"prompt": user_prompt}
    result = graph.invoke(initial_state)
    return result


if __name__ == "__main__":
    prompt = input("Enter your project idea: ")
    output = run_pipeline(prompt)
    print("\n=== Final Output ===")
    for key, val in output.items():
        print(f"\n[{key.upper()}]\n{val}\n")
