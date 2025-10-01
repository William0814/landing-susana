from dotenv import load_dotenv
import os
load_dotenv()
class TolgeeManager:
    def __init__(self, api_key, default_lang='de-DE', api_url=os.getenv('TOLGEE_API_URL'), tolgee_editor=os.getenv('TOLGEE_EDITOR', 'false')):
        self.api_key = api_key
        self.default_lang = default_lang
        self.api_url = api_url
        self.tolgee_editor = tolgee_editor

    def get_translation(self, lang=None):
        return {
            "tolgee_api_key": self.api_key,
            "tolgee_lang": lang or self.default_lang,
            "tolgee_api_url": self.api_url,
            "enable_Editor": self.tolgee_editor
        }