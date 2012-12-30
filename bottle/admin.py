from django.contrib import admin

from bottle.models import Bottle

class BottleAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['whisky']}),
    (None, {'fields': ['volume']}),
    (None, {'fields': ['price']}),
    (None, {'fields': ['volumeConsumedInitial']}),
    (None, {'fields': ['empty']}),
    ]
  list_display = ('pk', 'whisky', 'volume', 'price', 'volumeConsumedInitial', 'empty')
  list_filter = ['volume']
  search_fields = ['whisky']
  date_hierarchy = 'date'

admin.site.register(Bottle, BottleAdmin)
