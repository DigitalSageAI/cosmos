import json

from tg_bot.config.settings import TRANSLATIONS_FILE


class Translator:
    def __init__(self, translations_file: str, default_lang: str = "en"):
        self.default_lang = default_lang
        self.translations = self.load_translations(translations_file)


    def load_translations(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
             

    def get(self, key: str, lang: str, **kwargs):
        text = self.translations.get(key, {}).get(lang, None)
        if text is None:
            text = self.translations.get(key, {}).get(self.default_lang, key) 
        return text.format(**kwargs)  
    

translator = Translator(TRANSLATIONS_FILE)