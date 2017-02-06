from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from mezzanine.conf import settings
from mezzanine.core.views import direct_to_template
from base.views import staff_list, staff_teams_list

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns(
        "",
        # Change the admin prefix here to use an alternate URL for the
        # admin interface, which would be marginally more secure.
        ("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += patterns(
            '',
            url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
    )

urlpatterns += patterns(
        '',
        url("^$", 'AIC_site.views.index', name="home"),
        url("^team/", include('base.urls')),
        #url("^game/", include('game.urls')),
        #url("^staff/$", staff_list, name="staff_list"),
        #url("^staff/teams/$", staff_teams_list, name="staff_teams_list"),
        ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
