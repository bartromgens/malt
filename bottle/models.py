from django.db import models

from whisky.models import Whisky
from userprofile.models import UserProfile 

class Bottle(models.Model):
  whisky = models.ForeignKey(Whisky)
  volume = models.FloatField('volume', default=700.0)
  volumeConsumedInitial = models.FloatField('initially consumed', default=0.0)
  empty = models.BooleanField(default=False)
  buyer = models.ForeignKey(UserProfile, default=1)
  price = models.FloatField('price', default=0.0)
  
  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  def getActualVolume(self):
   
    from glass.models import Glass
    drinks = Glass.objects.filter(bottle__id=self.id)
    
    volumeDrunk = 0.0
    for drink in drinks:
      volumeDrunk += drink.volume
      
    actualVolume = self.volume - self.volumeConsumedInitial - volumeDrunk
    
    return actualVolume
  
  def getActualVolumeAll(self):
    bottles = Bottle.objects.order_by("volume")
    
    totalInStock_L = 0.0
    
    for bottle in bottles:
      if not bottle.empty:
        totalInStock_L += bottle.getActualVolume() / 1000.0
        
    return totalInStock_L
  
  def __unicode__(self):
    return str(self.whisky) + ' (#' + str(self.pk) + ')'
  
  class Meta:
    ordering = ['whisky']
  
  
def addBottleInfo(bottle):
  bottle.distillery = bottle.whisky.distillery
  bottle.volume_liters = '%.1f' % (bottle.volume / 1000.0)
  bottle.volumeActual = bottle.getActualVolume()
  bottle.age_int = int(bottle.whisky.age)
  bottle.alcoholPercentage_int = int(bottle.whisky.alcoholPercentage)
  bottle.percentageLeft = '%.0f' % (bottle.volumeActual/bottle.volume * 100.0)
  bottle.percentageGone = '%.0f' % (100 - (bottle.volumeActual/bottle.volume * 100.0))
  bottle.statusMeterWidth = '%.0f' % (bottle.volumeActual/bottle.volume * 75.0)
    
  return bottle

def addBottlesInfo(bottles):
  for bottle in bottles:
    addBottleInfo(bottle)
    
  return bottles