from django.conf.urls import patterns, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from glass.views import DrinksView
from glass.views import MyDrinksView
from glass.views import DrinksStatsView

urlpatterns = patterns('',
  url(r'^$', login_required(DrinksView.as_view())),
  url(r'^my/$', login_required(MyDrinksView.as_view())),
  url(r'^stats/$', login_required(DrinksStatsView.as_view())),
  url(r'^new/$', 'glass.views.new_drink'),
  url(r'^new/(?P<bottleId>\d+)$', 'glass.views.new_drink'),
  url(r'^plot/history.png$', 'glass.views.plot_drinks_volume_history'),
  url(r'^plot/historystack.png$', 'glass.views.plot_drinks_stacked_volume_history'),
#  url(r'^new/$', login_required(SelectGroupTransactionView.as_view())),
#  url(r'^new/(?P<groupAccountId>\d+)/$', 'transaction.views.newTransaction'),
)

#urlpatterns += staticfiles_urlpatterns()
