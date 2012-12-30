from base.views import BaseView
from bottle.models import Bottle

class CollectionView(BaseView):
  template_name = "collection/index.html"
  context_object_name = "transaction"
  
  def addBottleInfo(self, bottles):
    for bottle in bottles:
      bottle.distillery = bottle.whisky.distillery
      bottle.volume_liters = '%.1f L' % (bottle.volume / 1000.0)
      bottle.volumeActual = bottle.getActualVolume()
      bottle.percentageLeft = '%.0f' % (bottle.volumeActual/bottle.volume * 100.0)
      bottle.percentageGone = '%.0f' % (100 - (bottle.volumeActual/bottle.volume * 100.0))
      bottle.statusMeterWidth = '%.0f' % (bottle.volumeActual/bottle.volume * 75.0)
    
    return bottles
  
  def getAllBottles(self):
    bottles = Bottle.objects.order_by("date")

    bottles = self.addBottleInfo(bottles)
    return bottles
  
  def getStockBottles(self):
    bottles = Bottle.objects.filter(empty=False).order_by("date")
    
    bottles = self.addBottleInfo(bottles)
    return bottles
  
  def getEmptyBottles(self):
    bottles = Bottle.objects.filter(empty=True).order_by("date")

    bottles = self.addBottleInfo(bottles)
    return bottles
  
  def get_context_data(self, **kwargs):
    context = super(CollectionView, self).get_context_data(**kwargs)
    bottles = self.getAllBottles()
    context['full_collection_list'] = bottles
    
    context['collectionsection'] = True
    return context
  

class StockView(CollectionView):
  template_name = "collection/index.html"
  context_object_name = "transaction"
  
  def get_context_data(self, **kwargs):
    context = super(StockView, self).get_context_data(**kwargs)
    bottles = self.getStockBottles()
    context['full_collection_list'] = bottles
    
    context['collectionsection'] = True
    return context
  

class EmptyBottleView(CollectionView):
  template_name = "collection/index.html"
  context_object_name = "transaction"
  
  def get_context_data(self, **kwargs):
    context = super(EmptyBottleView, self).get_context_data(**kwargs)
    bottles = self.getEmptyBottles()
    context['full_collection_list'] = bottles
    
    context['collectionsection'] = True
    return context
    