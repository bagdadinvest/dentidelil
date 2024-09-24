from modeltranslation.translator import register, TranslationOptions
from .models import BlogPage, BlogIndexPage, AIContentTemplate

@register(BlogPage)
class BlogPageTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'body')

@register(BlogIndexPage)
class BlogIndexPageTranslationOptions(TranslationOptions):
    fields = ('title', 'intro')

@register(AIContentTemplate)
class AIContentTemplateTranslationOptions(TranslationOptions):
    fields = ('name', 'prompt_template')
