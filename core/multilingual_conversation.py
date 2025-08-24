from libretranslatepy import LibreTranslateAPI

class MultilingualConversationEngine:
    def __init__(self, base_engine):
        self.base_engine = base_engine
        self.lt = LibreTranslateAPI("https://libretranslate.de")  # public free server

    def generate(self, user_input: str) -> str:
        try:
            # Detect user language
            detected_lang = self.lt.detect(user_input)
            
            # Translate input to English for the AI if not English
            if detected_lang != "en":
                user_input_en = self.lt.translate(user_input, source=detected_lang, target="en")
            else:
                user_input_en = user_input

            # Generate AI response (in English)
            response_en = self.base_engine.generate(user_input_en)

            # Translate back to user's language
            if detected_lang != "en":
                response = self.lt.translate(response_en, source="en", target=detected_lang)
            else:
                response = response_en

            return response
        except Exception as e:
            return f"Oops! Something went wrong. (Error: {e})"
