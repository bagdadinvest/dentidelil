from django.db import models
from django.shortcuts import render, Http404
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel, PageChooserPanel
)
from wagtail.core.blocks import StructBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable, Locale, Site
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtailmedia.models import Media
from utils.models import LinkFields, RelatedLink, CarouselItem
from wagtail.images.models import Image
from django.utils.translation import gettext_lazy as _


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(_('Your Facebook page URL'), null=True, blank=True)
    instagram = models.URLField(_('Your Instagram URL'), max_length=255, null=True, blank=True)
    twitter = models.URLField(_('Your Twitter URL'), max_length=255, null=True, blank=True)
    youtube = models.URLField(_('Your YouTube Channel URL'), null=True, blank=True)
    linkedin = models.URLField(_('Your Linkedin URL'), max_length=255, null=True, blank=True)
    github = models.URLField(_('Your Github URL'), max_length=255, null=True, blank=True)
    facebook_appid = models.CharField(_('Your Facebook AppID'), max_length=255, null=True, blank=True)


@register_setting
class SiteBranding(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    site_name = models.CharField(_('Site Name'), max_length=250, null=True, blank=True)
    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('site_name'),
    ]


class HomePageContentItem(Orderable, LinkFields):
    page = ParentalKey('pages.HomePage', related_name='content_items')
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title = models.CharField(_('Title'), max_length=100)
    content = RichTextField(_('Content'), null=True, blank=True)
    summary = RichTextField(_('Summary'), blank=True)
    slug = models.SlugField(_('Slug'))

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.HomePage', related_name='carousel_items')


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.HomePage', related_name='related_links')


class HomePage(Page):
    background_video = models.ForeignKey('wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL,
                                         related_name='+')
    main_title = models.CharField(_('Main Title'), max_length=255, default="DENT I DELIL CLINIC")
    main_description = models.TextField(_('Main Description'),
                                        default="Your smile, our priority. Affordable dental care abroad.")
    portfolio_items = StreamField([
        ('portfolio_item', StructBlock([
            ('title', CharBlock(label=_('Title'), required=True)),
            ('subtitle', CharBlock(label=_('Subtitle'), required=False)),
            ('image', ImageChooserBlock(label=_('Image'), required=True)),
        ])),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        MediaChooserPanel('background_video'),
        FieldPanel('main_title'),
        FieldPanel('main_description'),
        StreamFieldPanel('portfolio_items'),
    ]

    class Meta:
        verbose_name = _("Home Page")

    def serve(self, request):
        site = Site.find_for_request(request)
        if not site:
            raise Http404("Site not found")

        current_locale = Locale.get_active()
        if not current_locale:
            raise Http404("Locale not found")

        try:
            root_page = Page.objects.get(depth=2, locale=current_locale, path__startswith=site.root_page.path)
        except Page.DoesNotExist:
            raise Http404("Root page not found for current locale")

        context = self.get_context(request)
        context['root_page'] = root_page
        return render(request, 'home.html', context)


class StandardIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    TEMPLATE_CHOICES = [
        ('pages/standard_index_page.html', 'Default Template'),
        ('pages/standard_index_page_grid.html', 'Grid Also In This Section'),
    ]
    subtitle = models.CharField(_('Subtitle'), max_length=255, blank=True)
    intro = RichTextField(_('Intro'), blank=True)
    template_string = models.CharField(
        max_length=255, choices=TEMPLATE_CHOICES,
        default='pages/standard_index_page.html'
    )
    feed_image = models.ForeignKey(
        Image,
        help_text=_("An optional image to represent the page"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('intro',)

    @property
    def template(self):
        return self.template_string


StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('template_string'),
    InlinePanel('related_links', label=_("Related links")),
]

StandardIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, _("Common page configuration")),
    ImageChooserPanel('feed_image'),
]


class StandardPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.StandardPage', related_name='related_links')


class StandardPage(Page):
    TEMPLATE_CHOICES = [
        ('pages/standard_page.html', 'Default Template'),
        ('pages/standard_page_full.html', 'Standard Page Full'),
    ]
    subtitle = models.CharField(_('Subtitle'), max_length=255, blank=True)
    intro = RichTextField(_('Intro'), blank=True)
    body = StreamField([
        ('paragraph', RichTextBlock(label=_('Paragraph'))),
        ('image', ImageChooserBlock(label=_('Image'))),
        ('html', RawHTMLBlock(label=_('HTML'))),
    ])
    template_string = models.CharField(
        max_length=255, choices=TEMPLATE_CHOICES,
        default='pages/standard_page.html'
    )
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    @property
    def template(self):
        return self.template_string


StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
    FieldPanel('template_string'),
    InlinePanel('carousel_items', label=_("Carousel items")),
    InlinePanel('related_links', label=_("Related links")),
]

StandardPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class VideoGalleryPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.VideoGalleryPage', related_name='carousel_items')


class VideoGalleryPage(Page):
    intro = RichTextField(_('Intro'), blank=True)
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]


VideoGalleryPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('carousel_items', label=_("Carousel items")),
]

VideoGalleryPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class TestimonialPage(Page):
    intro = RichTextField(_('Intro'), blank=True)
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]


TestimonialPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
]

TestimonialPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class ContentBlock(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='contentblocks',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(_('Title'), max_length=255)
    body = RichTextField(_('Body'))
    summary = RichTextField(_('Summary'), blank=True)
    slug = models.SlugField(_('Slug'))
    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        FieldPanel('summary'),
        FieldPanel('body', classname="full"),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return u"{0}[{1}]".format(self.title, self.slug)


register_snippet(ContentBlock)


class Testimonial(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='testimonials',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(_('Name'), max_length=150)
    photo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL
    )
    text = RichTextField(_('Text'), blank=True)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('name'),
        ImageChooserPanel('photo'),
        FieldPanel('text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return self.name


register_snippet(Testimonial)


class Advert(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='adverts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(_('Title'), max_length=150, null=True)
    image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL
    )
    button_text = models.CharField(_('Button Text'), max_length=150, null=True)
    text = RichTextField(_('Text'), blank=True)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('text'),
        FieldPanel('button_text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return self.title


register_snippet(Advert)


class FaqsPage(Page):
    body = StreamField([
        ('faq_question', CharBlock(label=_('FAQ Question'), classname="full title")),
        ('faq_answer', RichTextBlock(label=_('FAQ Answer'))),
    ])


FaqsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
]
