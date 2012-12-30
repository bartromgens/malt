from django.db import models

from bottle.models import Bottle
from userprofile.models import UserProfile

class Glass(models.Model):
  bottle = models.ForeignKey(Bottle)
  volume = models.FloatField('volume')
  user = models.ForeignKey(UserProfile)
  rating = models.IntegerField(default=-1, blank=True)

  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  
  def getPrice(self):
    return self.bottle.price * self.volume / self.bottle.volume
  
  def __unicode__(self):
    return str(self.volume) + '[ml] of ' + str(self.bottle)