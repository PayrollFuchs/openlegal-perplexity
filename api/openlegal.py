import requests
import json
from http.server import BaseHTTPRequestHandler

# ==== Trage hier deine beiden Keys ein ====
OLD_API_KEY = "433b35a27c350c36da96ae789c8ea0af5a7d6ba1"
PPLX_API_KEY = "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"
# ==========================================

def get_legal_data():
    """Holt aktuelle Fälle vom Open Legal Data API."""
    url = "https://de.openlegaldata.io/api/cases/?court_id=3"
    headers = {"api_key": OLD_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def ask_perplexity(prompt, context_data):
    """Schickt die Daten und Frage an die Perplexity API."""
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar-large-chat",  # alternativ: sonar-small-chat
        "messages": [
            {"role": "system", "content": "Du bist ein juristischer Rechercheassistent."},
            {"role": "user", "content": f"{prompt}\n\nHier sind die Daten:\n{json.dumps(context_data)}"}
        ]
    }
    response = requests.post("https://api.perplexity.ai/chat/completions",
                             headers=headers, json=data)
    return response.json()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Daten von Open Legal Data holen
        cases = get_legal_data()

        # 2. Perplexity fragen
        result = ask_perplexity("Fasse die neuesten Fälle zusammen", cases)

        # 3. HTTP-Antwort senden
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

