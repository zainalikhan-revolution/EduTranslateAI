# translator.py

from deep_translator import GoogleTranslator

def translate_text(text: str, target_language: str = "ur") -> str:
    """
    Translates text into the target language using Google Translator.
    
    Args:
        text (str): Original English text.
        target_language (str): Target language code (default: Urdu).

    Returns:
        str: Translated text.
    """
    translated = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated
