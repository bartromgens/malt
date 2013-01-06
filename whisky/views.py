from base.views import BaseView

from whisky.models import Whisky
from whisky.models import Distillery

class WhiskiesView(BaseView):
  template_name = "whiskies/index.html"

  def addExtraInfo(self, malts):
    for malt in malts:
      malt.alcoholPercentage_int = int(malt.alcoholPercentage)
  
  def getAllWhiskies(self):
    malts = Whisky.objects.order_by("date")

    self.addExtraInfo(malts)
    return malts
  
  def get_context_data(self, **kwargs):
    context = super(WhiskiesView, self).get_context_data(**kwargs)
    malts = self.getAllWhiskies()
    context['whiskies_list'] = malts
    
    context['whiskiessection'] = True
    return context
  

class DistilleriesView(BaseView):
  template_name = "distilleries/index.html"
  
  def getAllDistilleries(self):
    distilleries = Distillery.objects.order_by("date")

    return distilleries
  
  def get_context_data(self, **kwargs):
    context = super(DistilleriesView, self).get_context_data(**kwargs)
    distilleries = self.getAllDistilleries()
    context['distilleries_list'] = distilleries
    
    context['distilleriessection'] = True
    return context