from django.db import models

from django.contrib.auth.models import User

#users = User.objects.filter(groups__name='monkeys')

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    displayname = models.CharField(max_length=200)
    #settings = models.ForeignKey(UserSettings)

    def __str__(self):
        return self.displayname
