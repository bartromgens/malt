from django.db import models

from datetime import datetime

from whisky.models import Whisky
from userprofile.models import UserProfile 

class Bottle(models.Model):
  whisky = models.ForeignKey(Whisky)
  volume = models.FloatField('volume', default=700.0)
  volumeConsumedInitial = models.FloatField('initially consumed', default=0.0)
  empty = models.BooleanField(default=False)
  buyer = models.ForeignKey(UserProfile, default=1)
  price = models.FloatField('price', default=0.0)
  donation = models.BooleanField(default=False)
  
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
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
  
  def getActualValueAll(self):
    bottles = Bottle.objects.order_by("volume")
    
    totalValueStock = 0.0
    
    for bottle in bottles:
      if not bottle.empty:
        totalValueStock += bottle.getActualVolume() / bottle.volume * bottle.price
        
    return totalValueStock
  
  def getAveragePercentageNotEmpty(self):
    bottles = Bottle.objects.filter(empty=False)
    
    addBottlesInfo(bottles)
    averagePercentageLeft = 0.0
    
    for bottle in bottles:
      averagePercentageLeft += bottle.percentageLeft_int
  
    averagePercentageLeft = averagePercentageLeft / float(len(bottles))
    
    return averagePercentageLeft
  
  def __unicode__(self):
    name = str(self.whisky)    
    return name
  
  class Meta:
    ordering = ['whisky']
  
  
def addBottleInfo(bottle):
  bottle.distillery = bottle.whisky.distillery
  bottle.volume_liters = '%.1f' % (bottle.volume / 1000.0)
  bottle.volumeActual = bottle.getActualVolume()
  bottle.age_int = int(bottle.whisky.age)
  bottle.alcoholPercentage_int = int(bottle.whisky.alcoholPercentage)
  
  percentageLeft = 0.0
  percentageGone = 100.0
  statusMeterWidth = 0.0
  
  if (bottle.volume != 0.0):
    percentageLeft = bottle.volumeActual/bottle.volume * 100.0
    percentageGone = 100 - (bottle.volumeActual/bottle.volume * 100.0)
    statusMeterWidth = bottle.volumeActual/bottle.volume * 75.0 + 4
    
  if (percentageLeft < 0.0):
    statusMeterWidth = 0.0
    
  bottle.percentageLeft_int =  percentageLeft
  bottle.percentageLeft = '%.0f' % percentageLeft
  bottle.percentageGone = '%.0f' % percentageGone
  bottle.statusMeterWidth = '%.0f' % statusMeterWidth
    
  return bottle


def addBottlesInfo(bottles):
  for bottle in bottles:
    addBottleInfo(bottle)
    
  return bottles