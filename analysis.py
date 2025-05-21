import os
from openai import OpenAI
from typing import Dict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PHASES = [
    ("Sätt scenen", "Sammanfatta syfte, mål och trygghetsramar för samtalet."),
    ("Perspektiv & argument", "Lista vilka olika röster och argument som kom fram."),
    ("Fördjupa & strukturera", "Peka på mönster, orsaker och möjliga lösningar."),
    ("Åtgärdsplan", "Specificera konkreta nästa steg med ansvar och tidsram.")
]

class ConversationAnalyzer:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def analyze(self, transcript: str) -> Dict[str, str]:
        results = {}
        for phase, instruction in PHASES:
            system_prompt = f"""
Du är en samtalscoach som analyserar ett transkriberat möte mellan skolledare och lärare.
Fokusera endast på denna fas:
{phase}: {instruction}
Svara kortfattat och tydligt.
"""
            user_prompt = f"Här är transkriptionen av samtalet:\n\n'''{transcript}'''
Analysera enligt ovan."
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=400
            )
            results[phase] = response.choices[0].message.content.strip()
        return results 