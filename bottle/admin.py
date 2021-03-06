from django.contrib import admin

from bottle.models import Bottle

class BottleAdmin(admin.ModelAdmin):
    fieldsets = [
      (None, {'fields': ['whisky']}),
      (None, {'fields': ['collection']}),
      (None, {'fields': ['volume']}),
      (None, {'fields': ['price']}),
      (None, {'fields': ['buyer']}),
      (None, {'fields': ['volumeConsumedInitial']}),
      (None, {'fields': ['empty']}),
      (None, {'fields': ['donation']}),
      (None, {'fields': ['date']}),
      ]
    list_display = ('pk', 'whisky', 'collection', 'volume', 'price', 'buyer', 'volumeConsumedInitial', 'empty', 'donation', 'date')
    list_filter = ['volume']
    search_fields = ['whisky']
    date_hierarchy = 'date'

admin.site.register(Bottle, BottleAdmin)
