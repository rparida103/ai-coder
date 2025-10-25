AI Coder

AI Coder is an autonomous multi-agent system that generates Python code, unit tests, and deployment instructions from a user-provided prompt. It leverages LangGraph for agent orchestration and GPT-4o-mini via LangChain for AI-driven code generation.

The app provides a Streamlit-based web UI for seamless user interaction.

⸻

Table of Contents
	•	Features
	•	Architecture
	•	Agents
	•	Setup & Installation
	•	Deployment on Render
	•	Using the App UI
	•	Environment Variables
	•	Contributing
	•	License

⸻

Features
	•	Multi-agent workflow:
	•	Development Lead: Creates a high-level design from your prompt.
	•	Developer: Implements Python code based on the design.
	•	Test Engineer: Writes pytest-based unit tests.
	•	Deployer: Generates a deployment guide.
	•	Streamlit frontend with collapsible sections for Design, Code, Tests, and Deployment Guide.
	•	Easily deployable to free platforms like Render.
	•	Supports arbitrary project prompts — the agents handle detailed generation autonomously.

⸻

Architecture

<pre>
User Prompt
     │
     ▼
┌───────────────────┐
│   LangGraph Core  │
│ (Shared State &   │
│   Agent Orchestration)
└─────────┬─────────┘
          │
          ▼
 ┌───────────────────┐
 │ Development Lead  │
 │ Generates high-   │
 │ level design      │
 └─────────┬─────────┘
           │
           ▼
 ┌───────────────────┐
 │ Developer         │
 │ Writes Python     │
 │ code              │
 └─────────┬─────────┘
           │
           ▼
 ┌───────────────────┐
 │ Test Engineer     │
 │ Generates unit    │
 │ tests (pytest)    │
 └─────────┬─────────┘
           │
           ▼
 ┌───────────────────┐
 │ Deployer          │
 │ Deployment guide  │
 └───────────────────┘
           │
           ▼
        Output
</pre>

	•	LangGraph orchestrates agent nodes with a shared state.
	•	LLM (GPT-4o-mini) is invoked in each agent node via llm.invoke(prompt).
	•	Agents communicate via shared state: design → code → tests → deployment guide.
	•	Streamlit UI serves as the front-end for user input and displays generated outputs in collapsible sections.

⸻

Agents

Agent	Role
Development Lead	Generates high-level project design based on user prompt.
Developer	Writes Python implementation following the design plan.
Test Engineer	Creates unit tests using pytest.
Deployer	Provides a deployment guide, including instructions and dependencies.


⸻

Setup & Installation
	1.	Clone the repo:

git clone https://github.com/rparida103/ai-coder.git
cd ai-coder

	2.	Create a Python virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

	3.	Install dependencies:

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

	4.	Add .env file and add your OpenAI API key, only for local runs:

# Edit .env and add:
# OPENAI_API_KEY=your-openai-api-key


⸻

Deployment on Render
	1.	Log in to Render and create a new Web Service.
	2.	Connect your GitHub repository (ai-coder).
	3.	Configure the service:
	•	Root Directory: leave empty (repo root)
	•	Build Command: pip install -r requirements.txt
	•	Start Command:

streamlit run app.py --server.port $PORT --server.address 0.0.0.0


	•	Environment Variables: Add OPENAI_API_KEY with your key.

	4.	Click Create Web Service. Render will build, deploy, and provide a public URL.

Optional: Enable Auto-Deploy for continuous deployment on main branch pushes.

⸻

Using the App UI
	1.	Open the Streamlit URL (local or deployed).
	2.	Enter your project idea in the text area, e.g.,

Build a command-line Python tool that fetches real-time cryptocurrency prices and allows saving favorites locally.

	3.	Click Generate Project.
	4.	The UI will show the following collapsible sections:
	•	Design Plan: High-level architecture of the project.
	•	Generated Code: Python implementation.
	•	Unit Tests: pytest tests for your code.
	•	Deployment Guide: Instructions to run the code and dependencies.
	5.	Click the arrows on each section to minimize or expand as needed.
	6.	To generate a new project, enter a new prompt and click Generate Project again.

⸻

Environment Variables
	•	OPENAI_API_KEY: Your OpenAI API key (never commit to GitHub).
	•	Use Render Environment Variables for security in deployment.

⸻

Contributing
	1.	Fork the repository.
	2.	Create a new branch for your feature:

git checkout -b feature/my-feature

	3.	Commit changes and push:

git commit -am "Add new feature"
git push origin feature/my-feature

	4.	Open a Pull Request.

