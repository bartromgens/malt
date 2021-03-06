from __future__ import division
import datetime

from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from django.http import HttpResponse

from base.views import BaseView
from bottle.models import Bottle, add_bottle_info, add_bottles_info
from glass.models import Glass


class BottleView(BaseView):
    template_name = "collection/bottle.html"

    def get_context_data(self, **kwargs):
        context = super(BottleView, self).get_context_data(**kwargs)
        bottleId = kwargs['bottleId']
        bottle = Bottle.objects.get(id=bottleId)
        bottle = add_bottle_info(bottle)
        context['bottle'] = bottle
        context['collectionsection'] = True
        return context


class CollectionView(BaseView):
    template_name = "collection/index.html"

    def get_all_bottles(self):
        bottles = Bottle.objects.order_by("whisky")
        bottles = add_bottles_info(bottles)
        return bottles

    def get_stock_bottles(self):
        bottles = Bottle.objects.filter(empty=False).order_by("whisky")
        bottles = add_bottles_info(bottles)
        return bottles

    def get_empty_bottles(self):
        bottles = Bottle.objects.filter(empty=True).order_by("whisky")
        bottles = add_bottles_info(bottles)
        return bottles

    def get_overview_bottle_lists(self):
        bottlesList = []
        nPerRow = 13
        for i in range( 0, int(Bottle.objects.count()/nPerRow)+1 ):
            bottles = Bottle.objects.filter(empty=False).order_by("whisky")[(i*nPerRow):(i+1)*nPerRow]
            if bottles.count() != 0:
                add_bottles_info(bottles)
                bottlesList.append(bottles)
        return bottlesList

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        bottles = self.get_all_bottles()
        context['full_collection_list'] = bottles
        context['collectionsection'] = True
        return context


class StockView(CollectionView):
    template_name = "collection/index.html"

    def get_context_data(self, **kwargs):
        context = super(StockView, self).get_context_data(**kwargs)
        bottles = self.get_stock_bottles()
        context['full_collection_list'] = bottles
        total_in_stock_liter = Bottle.get_actual_volume_all()
        total_actual_value = Bottle.get_actual_value_all()
        average_percentage_not_empty = Bottle.get_average_percentage_not_empty()
        drinks = Glass.objects.all()

        total_drunk_ml = 0.0
        total_cost= 0.0

        n_bottles = Bottle.objects.filter(empty=False).count()
        n_drinks = drinks.count()

        for drink in drinks:
            total_drunk_ml += drink.volume
            total_cost += drink.get_price()

        total_in_stock_liter_str = '%.1f' % total_in_stock_liter

        context['totalInStock_L'] = total_in_stock_liter_str
        context['total_actual_value'] = total_actual_value
        if total_in_stock_liter != 0:
            context['value_per_700ml'] = total_actual_value / total_in_stock_liter * 0.7
        else:
            context['value_per_700ml'] = 0.0
        context['average_percentage_not_empty'] = average_percentage_not_empty
        context['totalDrunk_L'] = total_drunk_ml / 1000.0
        context['totalCost'] = total_cost
        context['nBottles'] = n_bottles
        context['nDrinks'] = n_drinks

        context['collectionsection'] = True
        return context


class EmptyBottleView(CollectionView):
    template_name = "collection/index.html"

    def get_context_data(self, **kwargs):
        context = super(EmptyBottleView, self).get_context_data(**kwargs)
        bottles = self.get_empty_bottles()
        context['full_collection_list'] = bottles
        context['collectionsection'] = True
        return context


class OverviewView(CollectionView):
    template_name = "collection/overview.html"

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        bottlesList = self.get_overview_bottle_lists()
        context['stock_lists'] = bottlesList
        context['collectionsection'] = True
        return context


def plot_bottle_history(request, bottleId):
    fig=Figure()
    canvas = FigureCanvas(fig)
    ax=fig.add_subplot(111)
    x=[]
    y=[]

    bottle = Bottle.objects.get(id=bottleId)
    drinks = Glass.objects.filter(bottle__id=bottleId)
    volumeInitial = bottle.volume - bottle.volumeConsumedInitial
    bottleDate = bottle.date
    now = datetime.datetime.now()

    x.append(bottleDate-datetime.timedelta(1))
    y.append(volumeInitial)

    for drink in drinks:
        x.append(drink.date)
        y.append(volumeInitial)
        volumeInitial -= drink.volume

    x.append(now)
    y.append(volumeInitial)

    ax.step(x, y, color='#106D2C', linewidth=2.0)

    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_label_text('Date')
    ax.yaxis.set_label_text('Volume [ml]')

    ax.set_ylim(0.0, bottle.volume - bottle.volumeConsumedInitial + 100)
    ax.set_xlim(bottleDate-datetime.timedelta(1), now)

    fig.autofmt_xdate()
    fig.set_facecolor('white')
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response


def get_bottles_user_pie_chart(request, bottleId):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')

    drinks = Glass.objects.filter(bottle__id=bottleId)

    drinksVolume = 0.0
    users = dict()
    labels = []
    fracs = []
    explode = []

    for drink in drinks:
        if drink.user in users:
            users[drink.user] = users[drink.user] + drink.volume
        else:
            users[drink.user] = drink.volume

        drinksVolume = drinksVolume + drink.volume

    for key in users:
        labels.append(key)
        fracs.append(users[key])
        explode.append(0.0)

    ax.pie(fracs, explode=explode, colors=('#87F881', '#8F96F4', '#FFDE85', '#FF8488', 'r', 'g', 'b'), \
             labels=labels, autopct='%1.0f%%', shadow=False)

    fig.set_facecolor('white')
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
