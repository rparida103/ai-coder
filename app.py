import streamlit as st
from backend.graph_builder import build_graph

st.set_page_config(page_title="AI Coder", layout="wide")
st.title("🤖 AI Coder – Autonomous Python Dev Agents")

# Initialize session state for results
if "result" not in st.session_state:
    st.session_state.result = None

user_prompt = st.text_area(
    "Enter your project idea:",
    placeholder="e.g., Build a REST API for task management",
    key="user_prompt",
)

col1, col2 = st.columns([1, 1])
with col1:
    run_button = st.button("Generate Project")
with col2:
    clear_button = st.button("Clear All")

# Clear outputs if Clear button is pressed
if clear_button:
    st.session_state.result = None
    st.session_state.user_prompt = ""

# Generate project if Run button is pressed
if run_button and user_prompt.strip():
    with st.spinner("Running multi-agent pipeline..."):
        graph = build_graph()
        state = {"prompt": user_prompt}
        st.session_state.result = graph.invoke(state)

# Display outputs if available
if st.session_state.result:
    result = st.session_state.result

    with st.expander("🧠 Design Plan", expanded=True):
        st.code(result["design_plan"], language="markdown")

    with st.expander("💻 Generated Code", expanded=True):
        st.code(result["code"], language="python")

    with st.expander("🧪 Unit Tests", expanded=False):
        st.code(result["tests"], language="python")

    with st.expander("🚀 Deployment Guide", expanded=False):
        st.code(result["deployment_guide"], language="markdown")
