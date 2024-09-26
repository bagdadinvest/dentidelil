from .base import BaseMachineTranslator
from wagtail_localize.strings import StringValue
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
import os

class CustomTranslator(BaseMachineTranslator):
    display_name = "Azure Translator"

    def __init__(self):
        # Initialize Azure Translator client
        self.client = TextTranslationClient(
            endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
        )

    def translate(self, source_locale, target_locale, strings):
        # Prepare content for Azure
        texts = [string.render_text() for string in strings]
        from_lang = source_locale.language_code
        to_lang = target_locale.language_code

        # Translate with Azure API
        response = self.client.translate(
            content=texts,
            to=[to_lang],
            from_parameter=from_lang
        )

        # Map results to original strings
        translations = {
            string: StringValue.from_plaintext(translation.text)
            for string, translation in zip(strings, response)
        }

        return translations

    def can_translate(self, source_locale, target_locale):
        return source_locale.language_code != target_locale.language_code
