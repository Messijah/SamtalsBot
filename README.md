# SamtalsBot

En AI-driven samtalsassistent för skolledare som:
- Spelar in och transkriberar gruppsamtal (Whisper)
- Analyserar innehållet enligt pedagogiska samtalsmodeller (GPT-4)
- Ger realtidsstöd och efterhandsrapport
- Stöder både text- och röstgränssnitt

## Kom igång
1. Klona projektet eller klistra in i Cursor.
2. Skapa ett virtuellt Python-env: `python -m venv venv && source venv/bin/activate`
3. Installera dependencies: `pip install -r requirements.txt`
4. Sätt din API-nyckel: `export OPENAI_API_KEY="din_nyckel"`
5. Testa inspelning och analys: `python main.py`
6. Starta servern för REST/WebSocket: `python server.py`

## Konfiguration
- Modifiera `SYSTEM_PROMPT` i `analysis.py` för att justera samtalsmodellen.
- Välj Whisper-modell i `transcription.py` för balans mellan hastighet och noggrannhet.

## Funktioner
- **Ljudinspelning**: Spelar in samtal med hög kvalitet
- **Transkribering**: Konverterar tal till text med Whisper
- **Analys**: Analyserar samtalet enligt pedagogiska samtalsmodeller
- **Realtidsstöd**: Ger tips och rekommendationer under samtalet
- **Text-till-tal**: Kan läsa upp sammanfattningar och analyser

## Säkerhet och integritet
- Alla inspelningar hanteras lokalt
- Ingen data sparas permanent utan explicit godkännande
- Möjlighet att köra helt offline (förutom GPT-analys) 