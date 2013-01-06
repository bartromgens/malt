from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from whisky.views import WhiskiesView
from whisky.views import DistilleriesView
from whisky.views import RegionsView

urlpatterns = patterns('',
  url(r'^$', login_required(WhiskiesView.as_view())),
  url(r'^distilleries/$', login_required(DistilleriesView.as_view())),
  url(r'^regions/$', login_required(RegionsView.as_view())),
#  url(r'^new/$', login_required(SelectGroupTransactionView.as_view())),
#  url(r'^new/(?P<groupAccountId>\d+)/$', 'transaction.views.newTransaction'),
)

#urlpatterns += staticfiles_urlpatterns()