from django.db import models

from datetime import datetime

class Region(models.Model):
  name = models.CharField(max_length=200)
  lat = models.FloatField('latitude', default='0.0')
  lon = models.FloatField('longitude', default='0.0')
  
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ['name']


class Distillery(models.Model):
  name = models.CharField(max_length=200)
  region = models.ForeignKey(Region)
  lat = models.FloatField('latitude', default='0.0')
  lon = models.FloatField('longitude', default='0.0')
  url = models.URLField(max_length=400, default='', blank=True)
  image = models.URLField(max_length=400, default='', blank=True)
  sound = models.BooleanField(default=False, blank=True)
  
  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  def __str__(self):
    return str(self.name)
  
  class Meta:
    ordering = ['name']


class Whisky(models.Model):
  distillery = models.ForeignKey(Distillery)
  name = models.CharField(max_length=200)
  age = models.FloatField('age')
  alcoholPercentage = models.FloatField('alcohol %')
  url = models.URLField(max_length=400, default='', blank=True) 
  
  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  def __str__(self):
    name = ''
    
    if (int(self.age) == 0):
      name = str(self.distillery)
    else:
      name = str(self.distillery) + '  ' + str(int(self.age))
    
    if self.name != 'normal':
      name = name + ' (' + self.name + ')'
 
    return name
  
  class Meta:
    ordering = ['distillery']