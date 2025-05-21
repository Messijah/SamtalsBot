import openai
import re
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class ConversationAnalyzer:
    def __init__(self, model="gpt-4"):
        self.model = model

    def analyze(self, transcript: str) -> dict:
        system_prompt = (
            "Du är en samtalscoach som analyserar ett möte utifrån fyra steg:\n"
            "1) Sätt scenen – sammanfatta syfte, mål och trygghetsramar.\n"
            "2) Perspektiv & argument – lista olika röster och argument.\n"
            "3) Fördjupa diskussionen – peka på mönster, orsaker och lösningar.\n"
            "4) Avsluta med konkreta åtgärder – specificera nästa steg.\n\n"
            "Gör en kort punktlista för varje steg baserat på transkriptionen."
        )
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system",  "content": system_prompt},
                {"role": "user",    "content": transcript},
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content
        phases = {}
        for header, body in re.findall(r"(\d\) [^\n]+)\n([\s\S]+?)(?=\n\d\)|\Z)", text):
            phases[header] = body.strip()
        return phases 