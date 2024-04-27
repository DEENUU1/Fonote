from typing import Optional

import deepl
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, lang_code: str):
        self.translator = deepl.Translator(settings.DEEPL_API_KEY)
        self.lang_code = lang_code

    def translate(self, text: str) -> Optional[str]:
        try:
            translated_text = self.translator.translate_text(text, target_lang=self.lang_code)
            return translated_text.text

        except Exception as e:
            logger.error(e)
            return
