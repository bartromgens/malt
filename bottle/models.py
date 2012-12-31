from django.db import models

from whisky.models import Whisky

class Bottle(models.Model):
  whisky = models.ForeignKey(Whisky)
  volume = models.FloatField('volume', default=700.0)
  volumeConsumedInitial = models.FloatField('initially consumed', default=0.0)
  empty = models.BooleanField(default=False)
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
  
  def __unicode__(self):
    return str(self.whisky) + ' (#' + str(self.pk) + ')'
  
