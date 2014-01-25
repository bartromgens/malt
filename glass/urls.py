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
  url(r'^new/$', 'glass.views.newDrink'),
  url(r'^new/mobile/$', 'glass.views.newDrinkMobile'),
  url(r'^plot/history.png$', 'glass.views.plotDrinksVolumeHistory'),
  url(r'^plot/historystack.png$', 'glass.views.plotDrinksStackedVolumeHistory'),
#  url(r'^new/$', login_required(SelectGroupTransactionView.as_view())),
#  url(r'^new/(?P<groupAccountId>\d+)/$', 'transaction.views.newTransaction'),
)

#urlpatterns += staticfiles_urlpatterns()