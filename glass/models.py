from django.db.models import signals

from datetime import datetime

from django.db import models
from bottle.models import Bottle, addBottleInfo
from userprofile.models import UserProfile

class Glass(models.Model):
  bottle = models.ForeignKey(Bottle)
  mass = models.FloatField('mass', default=0.0, blank=True)
  volume = models.FloatField('volume', default=50.0)
  user = models.ForeignKey(UserProfile)
  rating = models.IntegerField(default=-1, blank=True)

  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
  def getPrice(self):
    return self.bottle.price * self.volume / self.bottle.volume
  
  def __unicode__(self):
    return str(self.volume) + '[ml] of ' + str(self.bottle)


def addDrinkInfo(drink):
  drink.price = '%.2f' % drink.getPrice() 
  drink.volume_int = '%.0f' % drink.volume 
    
  return drink


def addDrinksInfo(drinks):
  date = datetime.today()
  for drink in drinks:
    drink = addDrinkInfo(drink)
    drink.bottle = addBottleInfo(drink.bottle)
    if drink.date.day < date.day:
      drink.isnewdate = True
    else:
      drink.isnewdate = False
    date = drink.date
      
  return drinks


def updateMassAndVolume(sender, **kwargs):
  drink = kwargs["instance"]
  
  alcoholPer = drink.bottle.whisky.alcoholPercentage
  waterPer = 100 - alcoholPer
  density = (1.0*waterPer + 0.789*alcoholPer) / 100.0
  
  if kwargs["created"]:
    if (drink.mass > 0):
      drink.volume = drink.mass * 1.0/density
      drink.save()
    else:
      drink.mass = drink.volume * density
      drink.save()

signals.post_save.connect(updateMassAndVolume, sender=Glass, dispatch_uid="drink_creation_signal")
