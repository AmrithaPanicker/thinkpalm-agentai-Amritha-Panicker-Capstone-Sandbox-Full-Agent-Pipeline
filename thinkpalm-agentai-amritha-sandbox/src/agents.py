from jira_tool import fetch_jira_ticket
from gherkin_generator import GherkinGenerator
from playwright_generator import PlaywrightGenerator
from coverage_analyzer import CoverageAnalyzer
from ai_engine import AIEngine
import os

# Initialize AI Engine (same as app.py)
api_key = os.getenv("OPENROUTER_API_KEY")
engine = AIEngine(api_key=api_key)

gherkin_gen = GherkinGenerator(engine)
playwright_gen = PlaywrightGenerator(engine)
coverage_anl = CoverageAnalyzer(engine)


def jira_agent(ticket_id):
    return fetch_jira_ticket(ticket_id)


def gherkin_agent(feature):
    return gherkin_gen.generate(feature, "General Flow")


def script_agent(gherkin):
    return playwright_gen.generate(gherkin, "General Flow")


def coverage_agent(feature, gherkin):
    return coverage_anl.analyze(feature, gherkin, "General Flow")