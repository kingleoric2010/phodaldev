from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
import mezzanine_pagedown.urls
from tastypie.api import Api
from blogapi.api import AllBlogSlugResource, BlogResource
from sitemaps.mobile_sitemaps import DisplayableSitemap as DisplayableMobileSitemap
from sitemaps.sitemaps import DisplayableSitemap
from sitemaps.sitemaps_https import DisplayableHTTPSSitemap

apiv1 = Api(api_name='v1')
apiv1.register(BlogResource())
apiv1.register(AllBlogSlugResource())

admin.autodiscover()

urlpatterns = i18n_patterns("",
    ("^admin/", include(admin.site.urls)),
)

if getattr(settings, "PACKAGE_NAME_FILEBROWSER") in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns("",
        ("^admin/media-library/", include("%s.urls" %
                                        settings.PACKAGE_NAME_FILEBROWSER)),
    )

sitemaps = {"sitemaps": {"all": DisplayableSitemap}}
sitemaps_https = {"sitemaps": {"all": DisplayableHTTPSSitemap}}
mobile_sitemaps = {"sitemaps": {"all": DisplayableMobileSitemap}}

urlpatterns += patterns("sitemaps.views",
    ("^sitemap\.xml$", "index", sitemaps),
    ("^sitemap_https\.xml$", "index", sitemaps_https),
    ("^sitemap_mobile\.xml$", "sitemap", mobile_sitemaps)
)

urlpatterns += patterns("feed.view",
   url("feeds/(?P<format>.*)%s$" % "/",
       "blog_post_feed", name="blog_post_feed"),
   url("^blog/feeds/(?P<format>.*)%s$" % "/",
       "blog_post_feed", name="blog_post_feed")
)

urlpatterns += patterns("homepage.views",
    url("^$", "homepage", name="home"),
)

urlpatterns += patterns('',
    url("^pagedown/", include(mezzanine_pagedown.urls)),
    url(r"^api/", include(apiv1.urls)),
    url(r"^api/app/", include("api.urls")),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),
    url("^", include("mezzanine.urls")),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"