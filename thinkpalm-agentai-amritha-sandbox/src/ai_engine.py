import requests
import json
import os

class AIEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    def call_openrouter_api(self, prompt, api_key=None):
        """
        Modular function to call OpenRouter API using requests library.
        """
        api_key = (api_key or self.api_key or "").strip()
        
        if not api_key:
            return "Error: OpenRouter API Key is missing. Please provide it in the .env file."

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("HTTP_REFERER", "http://localhost:8501"),
            "X-Title": os.getenv("X_TITLE", "AI Automation Assistant")
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a test automation assistant"},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "Error: Received empty response from OpenRouter."
            else:
                return f"Error: API Request failed with status code {response.status_code}. Details: {response.text}"
        
        except requests.exceptions.Timeout:
            return "Error: The request timed out. Please try again."
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"

    def generate_content(self, prompt):
        # Wrapper to maintain compatibility with existing generator calls
        return self.call_openrouter_api(prompt)

# Singleton instance (though we will pass API key from UI)
ai_engine = AIEngine()
