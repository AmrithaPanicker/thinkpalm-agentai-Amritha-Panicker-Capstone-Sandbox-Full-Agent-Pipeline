# thinkpalm-agentai-Amritha-Panicker-Capstone-Sandbox-Full-Agent-Pipeline
# AI-Powered Test Automation Assistant (Agentic AI Sandbox)

## Name

Amritha Panicker

## Track

QA / Testing

## Lab

Agentic AI Sandbox

---

## Project Overview

This project is an **AI-powered Test Automation Assistant** that uses an **Agentic AI pipeline** to automate the software testing process.

The system is capable of:

* Reading feature descriptions directly from Jira (via API)
* Generating BDD test cases in Gherkin format
* Creating Playwright automation scripts
* Identifying coverage gaps in testing
* Storing and reusing previous executions using persistent memory

This solution demonstrates how multiple AI agents can collaborate to solve a real-world QA automation problem.

---

## Agentic Architecture

The system is designed using multiple specialized agents:

* **Jira Agent**
  Fetches feature descriptions from Jira using REST API (Tool Calling)

* **Gherkin Agent**
  Converts feature descriptions into BDD test scenarios

* **Script Agent**
  Generates Playwright automation scripts based on Gherkin

* **Coverage Agent**
  Analyzes test coverage and identifies missing edge cases

---

## ReAct Loop Implementation

The system follows a simplified **ReAct (Reasoning + Acting)** approach:

1. Generate initial test cases
2. Analyze coverage gaps
3. If gaps are detected → regenerate improved test cases
4. Continue with automation script generation

This ensures better quality and completeness of generated tests.

---

## Memory Implementation

Persistent memory is implemented using **SQLite database**:

* Stores previous test generations
* Maintains timestamp (`created_at`) for each execution
* Retrieves latest entries for reuse
* Enhances current execution using past context

This allows the system to **learn from previous runs** and improve future outputs.

---

## Tools & Technologies Used

* **Streamlit** → UI for user interaction
* **Jira REST API** → Tool calling for feature extraction
* **OpenRouter AI (GPT-4o-mini)** → LLM for generation
* **SQLite** → Persistent memory storage
* **Python** → Core development

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd thinkpalm-agentai-amritha-sandbox
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root folder:

```text
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
JIRA_URL=your_jira_url
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_token
```

### 4. Run the Application

```bash
streamlit run src/app.py
```

### 5. Access in Browser

```
http://localhost:8501
```

---

## Screenshots

Refer to the `/screenshots` folder for:

* Jira-based test generation
* Gherkin output
* Playwright script generation
* Coverage analysis

---

## Observations

* Agent-based architecture improves modularity and scalability
* Tool calling (Jira API) makes the system more practical and real-world applicable
* ReAct loop helps improve test coverage iteratively
* Persistent memory (SQLite) enables reuse of past results and enhances output quality
* Combining multiple agents leads to better separation of concerns and maintainability

---

## Conclusion

This project successfully demonstrates an **end-to-end agentic pipeline** for QA automation using:

* Multi-agent collaboration
* Tool integration
* Persistent memory
* Iterative reasoning (ReAct)

It can be extended further into a production-grade AI-assisted testing system.
