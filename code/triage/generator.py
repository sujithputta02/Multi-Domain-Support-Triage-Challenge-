import requests
import json
import re

class OllamaGenerator:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
        self.is_available = self._check_availability()

    def _check_availability(self):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def generate_response(self, query, context, domain):
        if not self.is_available:
            return None
        
        # Aggressively clean context to save tokens and speed up inference
        clean_context = re.sub(r'---.*?---', '', context, flags=re.DOTALL)
        clean_context = re.sub(r'\n+', '\n', clean_context).strip()
        
        prompt = f"""
You are a professional support agent for {domain}. 
Answer the user's question based ONLY on the provided documentation.

STRICT RULES:
1. Use ONLY the information in the Context.
2. If the answer isn't there, say "I don't have enough information in our current documentation to answer that."
3. Be polite and concise.
4. DO NOT use markdown formatting (no **, no *, no #). 
5. Provide clean, plain text only.
6. Use numbered lists (1. 2. 3.) for steps.

USER QUESTION: {query}

CONTEXT:
{clean_context}

RESPONSE:
"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "top_p": 0.9}
        }
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            text = response.json().get('response', '').strip()
            # AGGRESSIVE REGEX to strip all markdown stars (* and **)
            text = re.sub(r'\*+', '', text)
            return text
        except Exception as e:
            return f"Error generating response: {e}"

    def classify(self, text, categories, context_type="intent"):
        prompt = f"""
Analyze and classify this ticket into EXACTLY ONE category: {', '.join(categories)}

TICKET:
{text}

Respond with ONLY the category name.
"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        }
        try:
            response = requests.post(self.url, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json().get('response', '').strip().lower()
            for cat in categories:
                if cat.lower() in result:
                    return cat
            return categories[0] if categories else "unknown"
        except Exception:
            return "unknown"

    def verify_relevance(self, query, context):
        return True
