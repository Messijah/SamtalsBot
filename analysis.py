import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ConversationAnalyzer:
    def __init__(self, model="gpt-4o-mini"):
        self.client = client
        self.model = model

    def analyze(self, transcript: str) -> dict:
        system_prompt = (
            "Du är en expert på att analysera professionella gruppsamtal i skolan enligt LPGD-modellen.\n"
            "Dela upp analysen i följande fyra huvudfaser, och för varje fas, använd de angivna subkategorierna.\n"
            "Ge både en sammanfattning och kodning av ledarens handlingar (ange citat/exempel där det är möjligt):\n\n"
            "1) Sätt scenen\n"
            "- a) Ställa frågor\n"
            "- b) Definiera problemet\n"
            "- c) Uppmuntra idéer från gruppen\n\n"
            "2) Bjud in olika perspektiv & argument\n"
            "- a) Ställa frågor\n"
            "- b) Ge information\n"
            "- c) Ge argument\n"
            "- d) Hålla gruppen på rätt spår\n\n"
            "3) Fördjupa diskussionen\n"
            "- a) Sammanfatta slutsatser\n"
            "- b) Klargöra reflektioner\n"
            "- c) Länka, kombinera och samstämma olika synpunkter\n\n"
            "4) Avsluta & summera\n"
            "- a) Gå igenom diskussionen\n"
            "- b) Sammanfatta uppgifter/åtgärder\n"
            "- c) Göra handlingsplan\n"
            "- d) Säkerställa ansvar och deadlines\n"
            "- e) Be om feedback på processen\n\n"
            "För varje fas och subkategori:\n"
            "- Ange om och hur ledaren agerade inom subkategorin (med citat/exempel om möjligt).\n"
            "- Sammanfatta vad som sades och hur processen gick till.\n"
            "- Om något saknas, skriv 'Ej observerat'.\n\n"
            "Avsluta med en kort reflektion:\n"
            "- Hur väl följdes LPGD-modellen?\n"
            "- Vilka styrkor/svagheter visade ledaren?\n"
            "- Förslag på förbättringar."
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
            temperature=0.2,
        )
        text = response.choices[0].message.content
        phases = {}
        for header, body in re.findall(r"(\d\) [^\n]+)\n([\s\S]+?)(?=\n\d\)|\Z)", text):
            phases[header] = body.strip()
        return phases 