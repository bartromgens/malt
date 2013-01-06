from __future__ import division
from base.views import BaseView
from bottle.models import Bottle

class CollectionView(BaseView):
  template_name = "collection/index.html"
  
  def addBottleInfo(self, bottles):
    for bottle in bottles:
      bottle.distillery = bottle.whisky.distillery
      bottle.volume_liters = '%.1f' % (bottle.volume / 1000.0)
      bottle.volumeActual = bottle.getActualVolume()
      bottle.age_int = int(bottle.whisky.age)
      bottle.alcoholPercentage_int = int(bottle.whisky.alcoholPercentage)
      bottle.percentageLeft = '%.0f' % (bottle.volumeActual/bottle.volume * 100.0)
      bottle.percentageGone = '%.0f' % (100 - (bottle.volumeActual/bottle.volume * 100.0))
      bottle.statusMeterWidth = '%.0f' % (bottle.volumeActual/bottle.volume * 75.0)
    
    return bottles
  
  def getAllBottles(self):
    bottles = Bottle.objects.order_by("whisky")

    bottles = self.addBottleInfo(bottles)
    return bottles
  
  def getStockBottles(self):
    bottles = Bottle.objects.filter(empty=False).order_by("whisky")
    
    bottles = self.addBottleInfo(bottles)
    return bottles
  
  def getEmptyBottles(self):
    bottles = Bottle.objects.filter(empty=True).order_by("whisky")

    bottles = self.addBottleInfo(bottles)
    return bottles
  
  def getOverviewBottleLists(self):
    bottlesList = []
    nPerRow = 13
    for i in range( 0, int(Bottle.objects.count()/nPerRow)+1 ):
      bottles = Bottle.objects.filter(empty=False).order_by("whisky")[(i*nPerRow):(i+1)*nPerRow]
      if bottles.count() != 0:
        self.addBottleInfo(bottles)
        bottlesList.append(bottles)
    
    return bottlesList
  
  def get_context_data(self, **kwargs):
    context = super(CollectionView, self).get_context_data(**kwargs)
    bottles = self.getAllBottles()
    context['full_collection_list'] = bottles
    
    context['collectionsection'] = True
    return context
  

class StockView(CollectionView):
  template_name = "collection/index.html"
  
  def get_context_data(self, **kwargs):
    context = super(StockView, self).get_context_data(**kwargs)
    bottles = self.getStockBottles()
    context['full_collection_list'] = bottles
    
    context['collectionsection'] = True
    return context
  

class EmptyBottleView(CollectionView):
  template_name = "collection/index.html"
  
  def get_context_data(self, **kwargs):
    context = super(EmptyBottleView, self).get_context_data(**kwargs)
    bottles = self.getEmptyBottles()
    context['full_collection_list'] = bottles
    
    context['collectionsection'] = True
    return context
  
  
class OverviewView(CollectionView):
  template_name = "collection/overview.html"
  
  def get_context_data(self, **kwargs):
    context = super(OverviewView, self).get_context_data(**kwargs)
    bottlesList = self.getOverviewBottleLists()
    context['stock_lists'] = bottlesList
    
    context['collectionsection'] = True
    return context
    