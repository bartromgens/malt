from whisky.models import Whisky
from collection.models import Collection
from userprofile.models import UserProfile
from base.settings import APP_DIR, STATIC_URL

from django.db import models

import os.path 
from datetime import datetime


class Bottle(models.Model):
    whisky = models.ForeignKey(Whisky)
    collection = models.ForeignKey(Collection, null=True, blank=True)
    volume = models.FloatField('volume', default=700.0)
    volumeConsumedInitial = models.FloatField('initially consumed', default=0.0)
    empty = models.BooleanField(default=False)
    buyer = models.ForeignKey(UserProfile, default=1)
    price = models.FloatField('price', default=0.0)
    donation = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    def get_actual_volume(self):
        from glass.models import Glass
        drinks = Glass.objects.filter(bottle__id=self.id)
        volume_drunk = 0.0
        for drink in drinks:
            volume_drunk += drink.volume
        actual_volume = self.volume - self.volumeConsumedInitial - volume_drunk
        return actual_volume

    @staticmethod
    def get_actual_volume_all():
        bottles = Bottle.objects.order_by("volume")
        total_instock_liter = 0.0
        for bottle in bottles:
            if not bottle.empty:
                total_instock_liter += bottle.get_actual_volume() / 1000.0
        return total_instock_liter

    @staticmethod
    def get_actual_value_all():
        bottles = Bottle.objects.order_by("volume")
        total_value_stock = 0.0
        for bottle in bottles:
            if not bottle.empty:
                total_value_stock += bottle.get_actual_volume() / bottle.volume * bottle.price
        return total_value_stock

    @staticmethod
    def get_average_percentage_not_empty():
        bottles = Bottle.objects.filter(empty=False)
        add_bottles_info(bottles)
        average_percentage_left = 0.0
        for bottle in bottles:
            average_percentage_left += bottle.percentageLeft_int
        if len(bottles) != 0:
            average_percentage_left /= float(len(bottles))
        return average_percentage_left

    def __str__(self):
        name = str(self.whisky)
        return name

    class Meta:
        ordering = ['whisky']


def add_bottle_info(bottle):
    bottle.distillery = bottle.whisky.distillery
    bottle.volume_liters = '%.1f' % (bottle.volume / 1000.0)
    bottle.volumeActual = bottle.get_actual_volume()
    bottle.age_int = int(bottle.whisky.age)
    bottle.alcoholPercentage_int = int(bottle.whisky.alcoholPercentage)

    percentage_left = 0.0
    percentage_gone = 100.0
    status_meter_width = 0.0

    if bottle.volume != 0.0:
        percentage_left = bottle.volumeActual/bottle.volume * 100.0
        percentage_gone = 100 - (bottle.volumeActual/bottle.volume * 100.0)
        status_meter_width = bottle.volumeActual/bottle.volume * 75.0 + 4

    if percentage_left < 0.0:
        status_meter_width = 0.0

    bottle.percentageLeft_int = percentage_left
    bottle.percentageLeft = '%.0f' % percentage_left
    bottle.percentageGone = '%.0f' % percentage_gone
    bottle.statusMeterWidth = '%.0f' % status_meter_width
    imagename = APP_DIR + 'static/images/bottles/' + str(bottle.whisky.distillery) + str(bottle.age_int) + '.jpg'
    if os.path.isfile(imagename):
        bottle.imagename = STATIC_URL + 'images/bottles/' + str(bottle.whisky.distillery) + str(bottle.age_int) + '.jpg'
    else:
        bottle.imagename = STATIC_URL + 'images/bottles/unknown.jpg'
    return bottle


def add_bottles_info(bottles):
    for bottle in bottles:
        add_bottle_info(bottle)
    return bottles
