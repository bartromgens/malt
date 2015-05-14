from matplotlib.figure import Figure
#from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from datetime import timedelta

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect

#from itertools import chain
from base.forms import LoginForm, UserCreateForm
from bottle.models import Bottle, add_bottles_info
from glass.models import Glass, add_drinks_info
from userprofile.models import UserProfile
import logging


class BaseView(TemplateView):
    template_name = "base/base.html"
    context_object_name = "base"

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BaseView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            userProfile = UserProfile.objects.get(user=self.request.user)
            context['user'] = self.request.user
            context['displayname'] = userProfile.displayname
            context['isLoggedin'] = True
            context['friends'] = UserProfile.objects.all()
        return context


class BaseUpdateView(UpdateView):
    template_name = "base/base.html"
    context_object_name = "base"

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BaseUpdateView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            userProfile = UserProfile.objects.get(user=self.request.user)
            context['user'] = self.request.user
            context['displayname'] = userProfile.displayname
            context['isLoggedin'] = True
        return context


class HomeView(BaseView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomeView, self).get_context_data(**kwargs)
#    user = self.request.user

        from bottle.views import CollectionView
        collectionView = CollectionView()

        totalInStock_L = Bottle.get_actual_volume_all(Bottle())
        totalActualValue = Bottle.get_actual_value_all(Bottle())
        averagePercentageNotEmpty = Bottle.get_average_percentage_not_empty(Bottle())
        drinks = Glass.objects.all()

        totalDrunk_ml = 0.0
        totalCost = 0.0

        nBottles = Bottle.objects.filter(empty=False).count()
        nDrinks = drinks.count()

        for drink in drinks:
            totalDrunk_ml += drink.volume
            totalCost += drink.get_price()

        totalInStock_L_str = '%.1f' % totalInStock_L

        bottlesList = CollectionView.get_overview_bottle_lists(collectionView)
        context['stock_lists'] = bottlesList
        context['totalInStock_L'] = totalInStock_L_str
        context['total_actual_value'] = totalActualValue
        if totalInStock_L != 0:
            context['value_per_700ml'] = totalActualValue / totalInStock_L * 0.7
        else:
            context['value_per_700ml'] = 0.0
        context['average_percentage_not_empty'] = averagePercentageNotEmpty
        context['totalDrunk_L'] = totalDrunk_ml / 1000.0
        context['totalCost'] = totalCost
        context['nBottles'] = nBottles
        context['nDrinks'] = nDrinks
        context['homesection'] = True

#    userProfile = UserProfile.objects.get(user=user)
        return context


class AboutView(BaseView):
    template_name = "base/about.html"
    context_object_name = "about"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AboutView, self).get_context_data(**kwargs)
        context['aboutsection'] = True
        return context


class HelpView(BaseView):
    template_name = "base/help.html"
    context_object_name = "help"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HelpView, self).get_context_data(**kwargs)
        context['helpsection'] = True

        return context


class TestView(BaseView):
    template_name = "base/test.html"
    context_object_name = "test"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TestView, self).get_context_data(**kwargs)
        return context


class Event():
    def __init__(self):
        self.date = ''
        self.volume = 0.0
        self.volume_str = ''
        self.cost = 0.0
        self.cost_str = ''
        self.drinks = []
        self.drinkers = set()
        self.bottles = set()
        self.nDrinks = 0
        self.tempID = 0

    def add_drink(self, drink):
        self.drinks.append(drink)
        self.volume += drink.volume
        self.cost += drink.get_price()
        self.drinkers.add(drink.user.displayname)
        self.bottles.add(drink.bottle)

    def add_info(self):
        self.bottles = add_bottles_info(self.bottles)


def get_events():
    drinks = Glass.objects.order_by('-date')
    events = []

    eventID = 1
    j = 0
    nDrinks = len(drinks)
    while (j < nDrinks-1):
        event = Event()

        delta = timedelta(0, 3600*4)
        while (j+1 < nDrinks and drinks[j].date - delta < drinks[j+1].date):
            event.add_drink(drinks[j])
            j = j + 1

        event.add_drink(drinks[j])
        event.nDrinks = len(event.drinks)

        if (event.nDrinks > 1 and len(event.drinkers) > 1):
            event.volume_str = '%.0f' % event.volume
            event.cost_str = '%.2f' % event.cost

            event.date = drinks[j].date
            event.tempID = eventID
            eventID += 1
            event.add_info()
            events.append(event)
        j = j + 1

    return events


class Events(object):
    events = ''

    @staticmethod
    def get_events():
        if len(Events.events) > 0:
            return Events.events
        else:
            Events.events = get_events()
            return Events.events


class EventsView(BaseView):
    template_name = "base/events.html"
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)

        events = Events.get_events()

        context['events_list'] = events
        context['eventssection'] = True
        return context


class EventView(BaseView):
    template_name = "base/event.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        eventId = int(kwargs['eventId'])
        context = super(EventView, self).get_context_data(**kwargs)

        events = Events.get_events()

        selectedEvent = 0

        for event in events:
            event.drinks = add_drinks_info(event.drinks)
            if event.tempID == eventId:
                selectedEvent = event

        context['event'] = selectedEvent
        context['eventssection'] = True
        return context


def plot_volume_event_pie_chart(request, eventId):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')

    events = Events.get_events()

    selectedEvent = 0
    for event in events:
        if event.tempID == int(eventId):
            selectedEvent = event
            break

    drinks = selectedEvent.drinks

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


def plot_region_event_pie_chart(request, eventId):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')

    events = Events.get_events()

    selectedEvent = 0
    for event in events:
        if event.tempID == int(eventId):
            selectedEvent = event
            break

    drinks = selectedEvent.drinks

    drinksVolume = 0.0
    regions = dict()
    labels = []
    fracs = []
    explode = []


    for drink in drinks:
        region = drink.bottle.whisky.distillery.region
        if region in regions:
            regions[region] = regions[region] + drink.volume
        else:
            regions[region] = drink.volume

        drinksVolume = drinksVolume + drink.volume

    for key in regions:
        labels.append(key)
        fracs.append(regions[key])
        explode.append(0.0)

    ax.pie(fracs, explode=explode, colors=('#87F881', '#8F96F4', '#FFDE85', '#FF8488', 'r', 'g', 'b'), \
             labels=labels, autopct='%1.0f%%', shadow=False)

    fig.set_facecolor('white')
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response


def register(request):
    def errorHandle(error):
        context_new = {
            'error': error,
            'form': UserCreateForm(),
        }
        return render_to_response('base/register.html', context_new, RequestContext(request))

    if request.method == 'POST': # If the form has been submitted...
        form = UserCreateForm(request.POST) # A form bound to the POST data
#     if form.is_valid():
#       form.save()
#       context = RequestContext(request)
#       context['registered'] = True
#       return render_to_response('base/register.html', context)
#     else:
#       error = u'form is invalid'
#       return errorHandle(error)
        error = u'Registrations are currently closed! Sorry!'
        return errorHandle(error)
    else:
        form = UserCreateForm() # An unbound form
        context = {
            'form': form
        }
        return render_to_response('base/register.html', context, RequestContext(request))


def login(request):
    def errorHandle(error):
        context_new = {
            'error': error,
            'form': LoginForm(),
        }
        return render_to_response('base/login.html', context_new, RequestContext(request))

    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    auth.login(request, user)
                    return redirect('/collection/')
                else:
                    # Return a 'disabled account' error message
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                # Return an 'invalid login' error message.
                error = u'invalid login'
                return errorHandle(error)
        else:
            error = u'form is invalid'
            return errorHandle(error)
    else:
        context = {
            'form': LoginForm()
        }
        return render_to_response('base/login.html', context, RequestContext(request))


def logout(request):
    auth.logout(request)
    return redirect('/login/')
