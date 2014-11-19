from django.contrib import admin

from collection.models import Collection

class CollectionAdmin(admin.ModelAdmin):
    fieldsets = [
      (None, {'fields': ['name']}),
      (None, {'fields': ['bulk']}),
      (None, {'fields': ['virtual']}),
      (None, {'fields': ['owner']}),
      (None, {'fields': ['group']}),
      ]
    list_display = ('pk', 'name', 'bulk', 'virtual', 'date')
    date_hierarchy = 'date'

admin.site.register(Collection, CollectionAdmin)
