from django.db import models

from userprofile.models import UserProfile
from django.contrib.auth.models import Group


class Collection(models.Model):
  name = models.CharField(max_length=200)
  bulk = models.BooleanField(default=False)
  virtual = models.BooleanField(default=False)
  owner = models.ForeignKey(UserProfile, null=True, blank=True)
  group = models.ForeignKey(Group, null=True, blank=True)
  
  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ['name']
  
