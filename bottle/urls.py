from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from bottle.views import CollectionView
from bottle.views import StockView
from bottle.views import EmptyBottleView

urlpatterns = patterns('',
  url(r'^$', login_required(CollectionView.as_view())),
  url(r'^all/$', login_required(CollectionView.as_view())),
  url(r'^stock/$', login_required(StockView.as_view())),
  url(r'^empty/$', login_required(EmptyBottleView.as_view())),
#  url(r'^new/$', login_required(SelectGroupTransactionView.as_view())),
#  url(r'^new/(?P<groupAccountId>\d+)/$', 'transaction.views.newTransaction'),
)

#urlpatterns += staticfiles_urlpatterns()