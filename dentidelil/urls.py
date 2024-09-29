from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.images.views.serve import ServeView

from pages import views as pages_views
from search import views as search_views
from wagtail_feeds.feeds import (
    BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed
)
#from pages.views import set_language  # Replace `myapp` with the actual app name where your view is defined
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),  # Django admin, no language prefix
    url(r'^i18n/', include('django.conf.urls.i18n')),  # Language change url
    url(r'^documents/', include(wagtaildocs_urls)),
]
#url(r'^set_language/$', set_language, name='set_language'),

# Add i18n patterns to handle localization of URLs
urlpatterns += i18n_patterns(
    # Wagtail admin panel
    url(r'^admin/', include(wagtailadmin_urls)),

    # User and account URLs
    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # Search functionality
    url(r'^search/$', search_views.search, name='search'),

    # Document handling in Wagtail

    # Sitemap
    url(r'^sitemap\.xml$', sitemap),  # Corrected '^sitemap.xml$' to '^sitemap\.xml$'

    # Blog feeds
    url(r'^blog/feed/basic$', BasicFeed(), name='basic_feed'),
    url(r'^blog/feed/extended$', ExtendedFeed(), name='extended_feed'),

    # JSON feeds
    url(r'^blog/feed/basic.json$', BasicJsonFeed(), name='basic_json_feed'),
    url(r'^blog/feed/extended.json$', ExtendedJsonFeed(), name='extended_json_feed'),

    # Serve images
    url(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        ServeView.as_view(), name='wagtailimages_serve'
    ),

    # Rosita URL (ensure it exists)
    # Assuming 'rosita.urls' is the correct module for rosita paths

    # Fallback to Wagtail's page serving mechanism
    url(r'', include(wagtail_urls)),
)

# Error handling for server errors
handler500 = 'pages.views.error_500'

# Only include static and media file handling in DEBUG mode
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic.base import RedirectView

    # Serve static files
    urlpatterns += staticfiles_urlpatterns()

    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Handle favicon
    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(
            url=settings.STATIC_URL + 'favicon.ico', permanent=True)
            ),
    ]

    # Enable debug toolbar if installed
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
