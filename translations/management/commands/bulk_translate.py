# translations/management/commands/bulk_translate.py

from django.core.management.base import BaseCommand
from wagtail.core.models import Page, Locale  # Import Locale from wagtail.core.models for Wagtail Localize 1.1
from wagtail_localize.strings import StringValue  # Import StringValue to handle translatable strings
from translations.azure import AzureTranslator  # Import your custom Azure translator

class Command(BaseCommand):
    help = 'Bulk translate all translatable pages into a specified target locale'

    def add_arguments(self, parser):
        # Add a required argument for the target locale (e.g., "fr" for French)
        parser.add_argument(
            '--locale',
            type=str,
            required=True,
            help='Locale code for the target language (e.g., "fr", "es", "de").',
        )

    def handle(self, *args, **options):
        # Use local imports to avoid circular import issues
        from wagtail_localize.models import Translation, TranslationSource

        # Get the target locale code from the command arguments
        target_locale_code = options['locale']

        # Retrieve the target locale object using the language code
        try:
            target_locale = Locale.objects.get(language_code=target_locale_code)
        except Locale.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Locale '{target_locale_code}' does not exist."))
            return

        # Initialize the custom Azure translator
        translator = AzureTranslator()

        # Retrieve all live pages that are public (adjust filters as needed)
        translatable_pages = Page.objects.live().public()

        # Iterate through each translatable page
        for page in translatable_pages:
            # Skip the root page (depth=1)
            if page.depth == 1:
                continue

            # Create or get the translation source for each page
            translation_source, _ = TranslationSource.get_or_create_from_instance(page)

            # Check if a translation already exists for the target locale
            translation, created = Translation.objects.get_or_create(
                source=translation_source,
                target_locale=target_locale,
            )

            # Manually extract translatable fields from the page instance
            # Assuming the fields to translate are 'title' and 'body' (customize as per your model)
            source_strings = []
            if hasattr(page, 'title') and isinstance(page.title, str):
                source_strings.append(StringValue('title', page.title))
            if hasattr(page, 'body') and isinstance(page.body, str):
                source_strings.append(StringValue('body', page.body))

            # Perform machine translation using the Azure Translator
            self.stdout.write(f"Triggering translation for page '{page.title}' into '{target_locale_code}'...")
            translated_strings = translator.translate(
                source_locale=translation_source.locale,
                target_locale=target_locale,
                strings=source_strings,
            )

            # Save the translated strings back to the translation object
            for source_string, translated_string in translated_strings.items():
                translation.save_translated_string(source_string, translated_string)

            # Save the translated page instance
            translation.save_target_instance()

        self.stdout.write(self.style.SUCCESS(f"Successfully triggered bulk translation for all pages to '{target_locale_code}'"))
