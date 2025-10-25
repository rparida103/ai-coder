import streamlit as st
from backend.graph_builder import build_graph

st.set_page_config(page_title="AI Coder", layout="wide")
st.title("🤖 AI Coder – Autonomous Python Dev Agents")

user_prompt = st.text_area(
    "Enter your project idea:",
    placeholder="e.g., Build a REST API for task management",
)
run_button = st.button("Generate Project")

if run_button and user_prompt.strip():
    with st.spinner("Running multi-agent pipeline..."):
        graph = build_graph()
        state = {"prompt": user_prompt}
        result = graph.invoke(state)

    st.success("✅ Generation Complete!")

    # Collapsible sections using st.expander
    with st.expander("🧠 Design Plan", expanded=True):
        st.code(result["design_plan"], language="markdown")

    with st.expander("💻 Generated Code", expanded=True):
        st.code(result["code"], language="python")

    with st.expander("🧪 Generated Unit Tests", expanded=False):
        st.code(result["tests"], language="python")

    with st.expander("🚀 Deployment Guide", expanded=False):
        st.code(result["deployment_guide"], language="markdown")
