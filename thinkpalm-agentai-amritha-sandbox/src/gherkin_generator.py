from ai_engine import AIEngine

class GherkinGenerator:
    def __init__(self, ai_engine: AIEngine):
        self.ai = ai_engine

    def generate(self, feature_description, flow_name):
        prompt = f"""
        You are an expert QA Automation Engineer. Generate comprehensive Gherkin (BDD) test cases 
        for the following flow in the OrangeHRM application:
        
        Flow: {flow_name}
        Feature Description: {feature_description}
        URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

        Requirements:
        - Generate structured BDD scenarios using Feature, Scenario, Given, When, Then.
        - Include Positive scenarios (Happy Path).
        - Include Negative scenarios (Invalid inputs, error handling).
        - Include Edge cases (Max/Min limits, special characters).
        - Use clear and descriptive scenario titles.
        
        Output only the Gherkin syntax.
        """
        return self.ai.generate_content(prompt)
