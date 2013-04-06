from django.contrib import admin

from whisky.models import Whisky
from whisky.models import Distillery
from whisky.models import Region

class WhiskyAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['distillery']}),
    (None, {'fields': ['name']}),
    (None, {'fields': ['age']}),
    (None, {'fields': ['alcoholPercentage']}),
    (None, {'fields': ['url']}),
    ]
  list_display = ('distillery', 'name', 'age', 'alcoholPercentage', 'url')
  list_filter = ['age']
  search_fields = ['name']
  date_hierarchy = 'date'

admin.site.register(Whisky, WhiskyAdmin)


class DistilleryAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['name']}),
    (None, {'fields': ['region']}),
    (None, {'fields': ['lat']}),
    (None, {'fields': ['lon']}),
    (None, {'fields': ['sound']}),
    (None, {'fields': ['url']}),
    (None, {'fields': ['image']}),
    ]
  list_display = ('name', 'region', 'lat', 'lon', 'sound', 'url', 'image')
  search_fields = ['name']
  date_hierarchy = 'date'

admin.site.register(Distillery, DistilleryAdmin)


class RegionAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['name']}),
    (None, {'fields': ['lat']}),
    (None, {'fields': ['lon']}),
    ]
  list_display = ('name', 'lat', 'lon')
  search_fields = ['name']
  date_hierarchy = 'date'

admin.site.register(Region, RegionAdmin)
