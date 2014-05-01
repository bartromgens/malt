from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from base.views import HomeView, AboutView, HelpView, EventsView, EventView, TestView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^/$', login_required(HomeView.as_view())),
  url(r'^test/$', login_required(TestView.as_view())),
  url(r'^login/$', 'base.views.login'),
  url(r'^logout/$', 'base.views.logout'),
  url(r'^register/$', 'base.views.register'),
  url(r'^help/$', HelpView.as_view()),
  url(r'^events/$', login_required( EventsView.as_view()) ),
  url(r'^events/(?P<eventId>\d+)/$', login_required( EventView.as_view()) ),
  url(r'^events/plots/regions/(?P<eventId>\d+).png$', 'base.views.plotRegionEventPieChart'),
  url(r'^events/plots/volumepie/(?P<eventId>\d+).png$', 'base.views.plotVolumeEventPieChart'),
  url(r'^about/$', AboutView.as_view()),
  
  url(r'^userprofile/', include('userprofile.urls')),
  url(r'^drinks/', include('glass.urls')),
  url(r'^collection/', include('bottle.urls')),
  url(r'^whiskies/', include('whisky.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
