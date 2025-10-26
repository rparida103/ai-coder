import streamlit as st
from backend.graph_builder import build_graph
from agents.deployer import create_pr

st.set_page_config(page_title="DevSquad AI", layout="wide")
st.title("🤖 DevSquad AI – Multi-Agent Python Project Generator")

# Initialize session state
if "result" not in st.session_state:
    st.session_state.result = None
if "pr_link" not in st.session_state:
    st.session_state.pr_link = None
if "clear_counter" not in st.session_state:
    st.session_state.clear_counter = 0

# Text area for project idea
user_prompt = st.text_area(
    "Enter your project idea:",
    placeholder="e.g., Build a REST API for task management",
    value="", # Set to an empty default value
    # Use a dynamic key based on the counter
    key=f"user_prompt_{st.session_state.clear_counter}",
)

# Buttons row
col1, col2, _ = st.columns([0.2, 0.2, 1])
with col1:
    run_button = st.button("Generate Project")
with col2:
    clear_button = st.button("Clear All")

# Clear all logic
if clear_button:
    st.session_state.result = None
    st.session_state.pr_link = None
    st.session_state.clear_counter += 1
    st.rerun()

# Generate project
if run_button and user_prompt.strip():
    with st.spinner("Running multi-agent pipeline..."):
        graph = build_graph()
        state = {"prompt": user_prompt}
        result = graph.invoke(state)

        # Wrap code/tests into files if 'files' key is missing
        if "files" not in result:
            files = {}
            if "code" in result and result["code"]:
                files["app.py"] = result["code"]
            if "tests" in result and result["tests"]:
                files["tests/test_app.py"] = result["tests"]
            result["files"] = files

        st.session_state.result = result
        st.session_state.pr_link = None  # reset PR link for new generation

# Display outputs
if st.session_state.result:
    result = st.session_state.result

    # Show collapsible sections
    with st.expander("🧠 Design Plan", expanded=False):
        st.code(result.get("design_plan", ""), language="markdown")

    with st.expander("💻 Generated Code", expanded=False):
        for fname, content in result.get("files", {}).items():
            if not fname.startswith("tests/"):
                st.subheader(fname)
                st.code(content, language="python")

    with st.expander("🧪 Unit Tests", expanded=False):
        for fname, content in result.get("files", {}).items():
            if fname.startswith("tests/"):
                st.subheader(fname)
                st.code(content, language="python")

    with st.expander("🚀 Deployment Guide", expanded=False):
        st.code(result.get("deployment_guide", ""), language="markdown")

    # Optional: Create Pull Request button
    if st.button("Create Pull Request"):
        project_files = result.get("files", {}).copy()
        # Add README.md with deployment guide
        project_files["README.md"] = "# Auto-generated project\n" + result.get(
            "deployment_guide", ""
        )
        with st.spinner("Creating PR..."):
            pr_link = create_pr(
                pr_title="Add new Python project via DevSquad AI",
                code_files=project_files,
            )
            st.session_state.pr_link = pr_link

    # Show PR link if created
    if st.session_state.pr_link:
        st.success(
            f"✅ Pull Request created: " f"[View PR]({st.session_state.pr_link})"
        )

else:
    st.info(
        "Enter your project idea above and click "
        "**Generate Project** to see the results here."
    )

# Sticky Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 12px;
        color: #37474F;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 500;
        background-color: #f9f9f9;
        padding: 5px 0;
        border-top: 1px solid #e6e6e6;
        margin: 0;
    }
    .css-18e3th9 {padding-left:0; padding-right:0;}
    </style>
    <div class="footer">
        Created by Rakesh Parida | Powered by OpenAI
    </div>
    """,
    unsafe_allow_html=True,
)
