from openai import OpenAI

class ConversationAnalyzer:
    def __init__(self, model="gpt-4"):
        self.model = model

    def analyze(self, transcript: str) -> dict:
        system_prompt = (
            "Du är en samtalscoach som analyserar ett transkriberat möte mellan skolledare och lärare."
            " Använd följande struktur:\n"
            "1) Sätt scenen: sammanfatta syfte, mål och trygghetsramar.\n"
            "2) Perspektiv & argument: lista olika röster och argument.\n"
            "3) Fördjupning & struktur: peka på mönster, orsaker och lösningar.\n"
            "4) Åtgärdsplan: specificera konkreta nästa steg med ansvar och tidsram."
        )

        user_prompt = f'''
Här är transkriptionen av samtalet:

"""
{transcript}
"""
Analysera enligt system-prompten:
'''

        client = OpenAI()
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content
        return {"analysis": text} 