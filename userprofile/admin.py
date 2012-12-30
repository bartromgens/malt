from userprofile.models import UserProfile

from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['user']}),
    (None, {'fields': ['displayname']}),
  ]
    
#class AccountAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, {'fields': ['name']}),
        #(None, {'fields': ['owner']}),
        #(None, {'fields': ['friends']}),
    #]
    #list_display = ('name', 'owner',)

admin.site.register(UserProfile, UserProfileAdmin)

#admin.site.register(Account, AccountAdmin)
