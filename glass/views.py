from matplotlib.figure import Figure, Rectangle
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect

from base.views import BaseView

from bottle.models import Bottle
from glass.models import Glass, add_drinks_info
from glass.forms import NewDrinkForm
from userprofile.models import UserProfile

import numpy
import logging


class DrinksView(BaseView):
    template_name = "drinks/index.html"
    context_object_name = "drinks"

    def get_all_drinks(self, lastN=0):
        if lastN == 0:
            drinks = Glass.objects.order_by('-date')
        else:
            drinks = Glass.objects.order_by('-date')[:lastN]

        drinks = add_drinks_info(drinks)
        return drinks

    def get_my_drinks(self, userProfileId):
        drinks = Glass.objects.filter(user__id=userProfileId).order_by('-date')

        drinks = add_drinks_info(drinks)
        return drinks

    def get_context_data(self, **kwargs):
        context = super(DrinksView, self).get_context_data(**kwargs)
        drinks = self.get_all_drinks(100)
        context['all_drinks_list'] = drinks

        context['drinkssection'] = True
        return context


class MyDrinksView(DrinksView):
    template_name = "drinks/index.html"
    context_object_name = "drinks"

    def get_context_data(self, **kwargs):
        userProfile = UserProfile.objects.get(user=self.request.user)

        context = super(MyDrinksView, self).get_context_data(**kwargs)
        bottles = self.get_my_drinks(userProfile.id)
        context['all_drinks_list'] = bottles

        context['drinkssection'] = True
        return context


class DrinksStatsView(BaseView):
    template_name = "drinks/stats.html"
    context_object_name = "drinks stats"

    def get_context_data(self, **kwargs):
        context = super(DrinksStatsView, self).get_context_data(**kwargs)
        context['drinkssection'] = True
        return context


def plot_drinks_volume_history(request):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    x = []
    y = []

    drinks = Glass.objects.order_by('date')

    fig.suptitle("Volume history")

    volume = 0.0

    for drink in drinks:
        x.append(drink.date)
        y.append(volume)
        volume += drink.volume

    x.append(datetime.now())
    y.append(volume)

    ax.step(x, y, '-', color='#106D2C', linewidth=2.0)

    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_label_text('Date')
    ax.yaxis.set_label_text('Volume [ml]')

#  ax.set_ylim(0.0, bottle.volume - bottle.volumeConsumedInitial + 100)
#  ax.set_xlim(bottleDate-datetime.timedelta(1), now)

    fig.autofmt_xdate()
    fig.set_facecolor('white')
    response = HttpResponse(content_type='image/png')
    fig.savefig(response, format="png", dpi=100)

    return response


def plot_drinks_stacked_volume_history(request):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    x = []

    drinks = Glass.objects.order_by('date')
    users = UserProfile.objects.all()

    fig.suptitle("Volume history stack")

    volume = dict()
    y = numpy.zeros( (len(users)+1, len(drinks)+1) )

    i = 0
    for user in users:
        y[i,0] = 0.0
        volume[user] = 0.0
        i += 1

    j = 0
    for drink in drinks:
        userDrink = drink.user
        x.append(drink.date)
        i = 0
        for user in users:
            y[i,j] = volume[user]
            i += 1
        volume[userDrink] += drink.volume
        j += 1

    i = 0
    x.append(datetime.now())
    for user in users:
        y[i,j] = volume[user]
        i += 1

    y_stack = numpy.cumsum(y, axis=0)

    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']

    counter = 0
    for user in users:
        if not counter:
            ax.fill_between(x, 0.0, y_stack[counter,:], facecolor=colors[counter % len(colors)], alpha=0.6)
        else:
            ax.fill_between(x, y_stack[counter-1,:], y_stack[counter,:], facecolor=colors[counter % len(colors)], alpha=0.6)
        counter += 1

    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_label_text('Date')
    ax.yaxis.set_label_text('Volume [ml]')

    fig.autofmt_xdate()
    fig.set_facecolor('white')

    i = 0
    p = []
    userNames = []
    for user in users:
        p.append( Rectangle((0, 0), 1, 1, facecolor=colors[i % len(colors)] ) )
        userNames.append(user)
        i += 1
    ax.legend(p, userNames, loc='upper left')

    response = HttpResponse(content_type='image/png')
    fig.savefig(response, format="png", dpi=100)

    return response


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def new_drink(request, bottleId = 0):
    def errorHandle(error):
        kwargs = {'user': request.user, 'bottleId': bottleId}
        logger.error('error in new drink')
        form = NewDrinkForm(**kwargs)
        context = {
            'error': error,
            'form': form,
        }
        if request.user.is_authenticated():
            context += {
                'user': request.user,
                'isLoggedin': True,
                'drinkssection': True
            }
        return render_to_response('drinks/new.html', context, RequestContext(request))

    if request.method == 'POST': # If the form has been submitted...
        logger.error('post new drink')
        kwargs = {'user' : request.user}
        form = NewDrinkForm(request.POST, **kwargs) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            emptiesBottle = form.cleaned_data['emptiesBottle']
            if (emptiesBottle):
                bottle = form.cleaned_data['bottle']
                bottle.empty = True
                bottle.save()

            form.save()
            logging.error('saved')
            return redirect('/drinks/')
        else:
            error = u'form is invalid'
            logging.error(error)
            return errorHandle(error)

    else:
        logger.error('request new drink form')
        kwargs = {'user' : request.user, 'bottleId' : bottleId}
        form = NewDrinkForm(**kwargs) # An unbound form
        form.fields["bottle"].queryset = Bottle.objects.filter(empty=False)
        context = dict()
        context['form'] = form
        context['drinkssection'] = True

        if request.user.is_authenticated():
            context['user'] = request.user
            context['isLoggedin'] = True

        return render_to_response('drinks/new.html', context, RequestContext(request))
