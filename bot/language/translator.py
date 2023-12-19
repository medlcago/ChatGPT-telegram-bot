import os

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner


class Translator:
    def __init__(self):
        self.locales_path = os.path.join(os.path.dirname(__file__), 'locales')
        self.t_hub = TranslatorHub(
            locales_map={
                "en": ("en", "ru"),
                "ru": ("ru",)
            },
            translators=[
                FluentTranslator(
                    locale="en",
                    translator=FluentBundle.from_files(
                        locale="en-US",
                        filenames=[os.path.join(self.locales_path, 'en.ftl')],
                        use_isolating=False)
                ),
                FluentTranslator(locale="ru",
                                 translator=FluentBundle.from_files(
                                     locale="ru-RU",
                                     filenames=[os.path.join(self.locales_path, 'ru.ftl')],
                                     use_isolating=False
                                 )
                                 )],
            root_locale="ru")

    def __call__(self, language: str):
        return LocalizedTranslator(translator=self.t_hub.get_translator_by_locale(locale=language))


class LocalizedTranslator:
    def __init__(self, translator: TranslatorRunner):
        self.translator = translator

    def get(self, key: str, **kwargs) -> str:
        return self.translator.get(key, **kwargs)
