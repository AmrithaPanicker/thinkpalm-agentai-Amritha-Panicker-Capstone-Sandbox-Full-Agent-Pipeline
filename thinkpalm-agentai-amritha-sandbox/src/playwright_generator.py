from ai_engine import AIEngine

class PlaywrightGenerator:
    def __init__(self, ai_engine: AIEngine):
        self.ai = ai_engine

    def generate(self, gherkin_scenarios, flow_name):
        prompt = f"""
        You are an expert Playwright and Python Automation Engineer.
        Convert the following Gherkin scenarios into a production-ready Playwright Python script.
        
        Flow: {flow_name}
        Gherkin Scenarios:
        {gherkin_scenarios}

        Requirements:
        1. Use Playwright with Python synchronous or asynchronous (prefer sync for simplicity in demo).
        2. Implement using Page Object Model (POM) pattern.
        3. Use proper selectors for OrangeHRM (e.g., [name='username'], [name='password'], .oxd-button, etc.).
        4. Include setup (browser launch) and teardown.
        5. Add meaningful assertions and error handling.
        6. Organize the code into a clean, reusable structure.
        7. The script should run in Chrome browser.
        
        Output only the Python code. No additional explanation.
        """
        return self.ai.generate_content(prompt)
