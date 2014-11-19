from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from collection.views import CollectionView

urlpatterns = patterns('',
  url(r'^$', login_required(CollectionView.as_view())),
)

#urlpatterns += staticfiles_urlpatterns()
