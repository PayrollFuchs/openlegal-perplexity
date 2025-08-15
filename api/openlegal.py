import os
import json
import requests
from http.server import BaseHTTPRequestHandler

# Perplexity API Key aus Environment Variable
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
MODEL = "sonar-medium-chat"  # funktionierendes Modell

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not PERPLEXITY_API_KEY:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "PERPLEXITY_API_KEY not set"}).encode())
            return

        query = "Bundesdatenschutzgesetz"  # Beispiel-Abfrage, kann dynamisch angepasst werden

        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "prompt": query
        }

        response = requests.post(
            "https://api.perplexity.ai/v1/answers",
            headers=headers,
            json=payload
        )

        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.content)
