from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from base.views import HomeView, AboutView, HelpView, EventsView, EventView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^malt/$', login_required(HomeView.as_view())),
  url(r'^malt/login/$', 'base.views.login'),
  url(r'^malt/logout/$', 'base.views.logout'),
  url(r'^malt/register/$', 'base.views.register'),
  url(r'^malt/help/$', HelpView.as_view()),
  url(r'^malt/events/$', login_required( EventsView.as_view()) ),
  url(r'^malt/events/(?P<eventId>\d+)/$', login_required( EventView.as_view()) ),
  url(r'^malt/events/plots/regions/(?P<eventId>\d+).png$', 'base.views.plotRegionEventPieChart'),
  url(r'^malt/events/plots/volumepie/(?P<eventId>\d+).png$', 'base.views.plotVolumeEventPieChart'),
  url(r'^malt/about/$', AboutView.as_view()),
  
  url(r'^malt/userprofile/', include('userprofile.urls')),
  url(r'^malt/drinks/', include('glass.urls')),
  url(r'^malt/collection/', include('bottle.urls')),
  url(r'^malt/whiskies/', include('whisky.urls')),
  url(r'^malt/admin/', include(admin.site.urls)),
)
