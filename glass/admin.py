from django.contrib import admin

from glass.models import Glass

class GlassAdmin(admin.ModelAdmin):
    fieldsets = [
      (None, {'fields': ['bottle']}),
      (None, {'fields': ['volume']}),
      (None, {'fields': ['mass']}),
      (None, {'fields': ['user']}),
      (None, {'fields': ['rating']}),
      (None, {'fields': ['date']}),
      ]
    list_display = ('pk', 'bottle', 'volume', 'mass', 'user', 'rating', 'date')
    search_fields = ['bottle']
    date_hierarchy = 'date'

admin.site.register(Glass, GlassAdmin)
