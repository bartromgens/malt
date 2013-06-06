from base.views import BaseView

from collection.models import Collection

class CollectionView(BaseView):
  template_name = "collections/index.html"
  
  def get_context_data(self, **kwargs):
    context = super(CollectionView, self).get_context_data(**kwargs)
    collections = Collection.objects.all()
    context['collections'] = collections
    
    context['collectionssection'] = True
    return context