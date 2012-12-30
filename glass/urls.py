from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from glass.views import DrinksView
from glass.views import MyDrinksView

urlpatterns = patterns('',
  url(r'^$', login_required(DrinksView.as_view())),
  url(r'^my/$', login_required(MyDrinksView.as_view())),
#  url(r'^new/$', login_required(SelectGroupTransactionView.as_view())),
#  url(r'^new/(?P<groupAccountId>\d+)/$', 'transaction.views.newTransaction'),
)

#urlpatterns += staticfiles_urlpatterns()