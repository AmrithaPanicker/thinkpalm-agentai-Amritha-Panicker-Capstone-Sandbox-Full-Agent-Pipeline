from ai_engine import AIEngine

class CoverageAnalyzer:
    def __init__(self, ai_engine: AIEngine):
        self.ai = ai_engine

    def analyze(self, feature_description, generated_scenarios, flow_name):
        prompt = f"""
        You are a Test Architect specializing in Quality Assurance.
        Analyze the coverage of the generated test cases against the required flow.

        Flow: {flow_name}
        Feature Description: {feature_description}
        Generated Scenarios:
        {generated_scenarios}

        Identify missing gaps in the following areas:
        - Negative scenarios (Error conditions, boundary values)
        - Edge cases (Extreme inputs, unusual sequences)
        - Validation checks (Data integrity, UI consistency)
        - Role-based access scenarios (if applicable)

        Display the gaps clearly in bullet points with brief reasoning for each.
        If coverage is perfect (unlikely), mention that.
        """
        return self.ai.generate_content(prompt)
