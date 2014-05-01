from django.db import models


from whisky.models import Whisky
from collection.models import Collection
from userprofile.models import UserProfile 
from base.settings import APP_DIR, STATIC_ROOT, DEBUG

import os.path
from datetime import datetime


class Bottle(models.Model):
  whisky = models.ForeignKey(Whisky)
  collection = models.ForeignKey(Collection, null=True, blank=True)
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
  
    if (len(bottles) != 0):
      averagePercentageLeft = averagePercentageLeft / float(len(bottles))
    
    return averagePercentageLeft
  
  def __str__(self):
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
  imagename = APP_DIR + 'malt/static/images/bottles/' + str(bottle.whisky.distillery) + str(bottle.age_int) + '.jpg'
  
  prefix = STATIC_ROOT
  if DEBUG:
    prefix = APP_DIR + 'malt/static/'
    
  if os.path.isfile(imagename):
    bottle.imagename = prefix + 'images/bottles/' + str(bottle.whisky.distillery) + str(bottle.age_int) + '.jpg'
  else:
    bottle.imagename = STATIC_ROOT + 'images/bottles/unknown.jpg'

  return bottle


def addBottlesInfo(bottles):
  for bottle in bottles:
    addBottleInfo(bottle)
    
  return bottles
