from backend.llm_utils import llm
from github import Github, GithubException
import os
from datetime import datetime
import streamlit as st
from typing import Dict, Any


def deployer(state: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate a deployment guide for the given project files.
    """
    project_files = state.get("files", {})

    # Format all files into a single, readable string for the LLM
    files_summary = ""
    if project_files:
        files_summary += (
            "The project consists of the following files and directories:\n\n"
        )
        for filename, content in project_files.items():
            files_summary += f"--- FILE: {filename} ---\n"
            files_summary += f"{content}\n\n"
    else:
        files_summary = "No code or tests were generated for this project."

    prompt = f"""
    You are a professional DevOps engineer.

    Based on the file structure and contents provided below,
    write a simple, step-by-step deployment guide. The guide should cover:
    1. Setting up the environment (e.g., Python version, virtual environments).
    2. Listing dependencies (e.g., from requirements.txt or inferred).
    3. Instructions for running unit tests (using 'pytest').
    4. Instructions for running the main application
        (e.g., 'python main.py' or 'flask run').

    Format the deployment guide using clear Markdown sections and code blocks.

    Project Files:
    ---
    {files_summary}
    ---
    """

    result = llm.invoke(prompt)
    return {"deployment_guide": result.content}


def create_pr(pr_title, code_files, repo_name="rparida103/ai-projects"):
    """
    Create a new branch, commit generated files, and open a PR.
    Returns PR URL or None if failed.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        # Note: In a real environment,
        # you'd use st.error only if GITHUB_TOKEN is expected
        # to be set externally, which seems to be the case here.
        st.error("GITHUB_TOKEN not set in environment variables")
        return None

    g = Github(token)
    try:
        repo = g.get_repo(repo_name)
    except GithubException as e:
        st.error(f"Failed to access repo: {e.data['message']}")
        return None

    # Determine default branch
    default_branch = repo.default_branch
    try:
        source = repo.get_branch(default_branch)
    except GithubException as e:
        st.error(f"Default branch '{default_branch}' not found: {e.data['message']}")
        return None

    # Create new branch
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_name = f"autogen/{timestamp}"
    try:
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
    except GithubException as e:
        st.error(f"Failed to create branch: {e.data['message']}")
        return None

    # Commit files
    # This loop correctly handles the multi-file dictionary structure
    for filename, content in code_files.items():
        if filename.endswith("requirements.txt"):
            if not content.strip() or "# No external dependencies required" in content:
                continue

        try:
            repo.create_file(
                path=filename, message=pr_title, content=content, branch=branch_name
            )
        except GithubException as e:
            if e.status == 422:  # File exists, update it
                try:
                    existing_file = repo.get_contents(filename, ref=branch_name)
                    repo.update_file(
                        path=existing_file.path,
                        message=pr_title,
                        content=content,
                        sha=existing_file.sha,
                        branch=branch_name,
                    )
                except GithubException as inner_e:
                    st.error(
                        f"Failed to update file {filename}: "
                        f"{inner_e.data['message']}"
                    )
                    return None
            else:
                st.error(f"Failed to create file {filename}: {e.data['message']}")
                return None

    # Create PR
    try:
        pr = repo.create_pull(
            title=pr_title,
            body="Automated PR created by DevSquad AI Deployer",
            head=branch_name,
            base=default_branch,
        )
        return pr.html_url
    except GithubException as e:
        st.error(f"Failed to create PR: {e.data['message']}")
        return None
