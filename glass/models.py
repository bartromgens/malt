from django.db.models import signals

from datetime import datetime, timedelta

from django.db import models
from bottle.models import Bottle, add_bottle_info
from userprofile.models import UserProfile

class Glass(models.Model):
    bottle = models.ForeignKey(Bottle)
    mass = models.FloatField('mass', default=0.0, blank=True)
    volume = models.FloatField('volume', default=50.0)
    user = models.ForeignKey(UserProfile)
    rating = models.IntegerField(default=-1, blank=True)

    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    def get_price(self):
        return self.bottle.price * self.volume / self.bottle.volume

    def __str__(self):
        return str(self.volume) + '[ml] of ' + str(self.bottle)


def add_drink_info(drink):
    drink.price = '%.2f' % drink.get_price()
    drink.volume_int = '%.0f' % drink.volume

    return drink


def add_drinks_info(drinks):
    date = datetime.today()
    date += timedelta(2)
    for drink in drinks:
        drink = add_drink_info(drink)
        drink.bottle = add_bottle_info(drink.bottle)
        if drink.date.day < date.day or drink.date.month != date.month:
            drink.isnewdate = True
        else:
            drink.isnewdate = False
        date = drink.date

    return drinks


def update_mass_and_volume(sender, **kwargs):
    drink = kwargs["instance"]

    alcoholPer = drink.bottle.whisky.alcoholPercentage
    waterPer = 100 - alcoholPer
    density = (1.0*waterPer + 0.789*alcoholPer) / 100.0

    if kwargs["created"]:
        if (drink.mass > 0):
            drink.volume = drink.mass * 1.0/density
            drink.save()
        else:
            drink.mass = drink.volume * density
            drink.save()

signals.post_save.connect(update_mass_and_volume, sender=Glass, dispatch_uid="drink_creation_signal")
