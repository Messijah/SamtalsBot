import os
from openai import OpenAI
from typing import Dict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Du är en samtalscoach för skolledare. Analysera transkriptionen enligt samtalsmodell:
1) Sätt scenen – Hur definierades syfte och ram?
2) Perspektiv – Vilka röster och argument kom fram?
3) Fördjupning – Vilka mönster eller insikter identifierades?
4) Avslut – Vilka konkreta åtgärder och nästa steg beslutades?
Svara strukturerat under varje rubrik.
"""

class ConversationAnalyzer:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def analyze(self, transcript: str) -> Dict[str, str]:
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": transcript}
            ],
            temperature=0.3,
            max_tokens=800
        )
        content = response.choices[0].message.content
        return {"analysis": content} 