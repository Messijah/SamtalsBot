from analysis import ConversationAnalyzer

class LiveFeedback:
    def __init__(self, analyzer: ConversationAnalyzer):
        self.analyzer = analyzer

    def generate_tip(self, recent_transcript: str) -> str:
        """
        Analysera de senaste meningarna och ge ett kort tips:
        ex: "Ställ en öppnande fråga om lösningar nu." 
        """
        result = self.analyzer.analyze(recent_transcript)
        # Extrahera bara en mening som tips från analysen
        return result["analysis"].split("\n")[0] 