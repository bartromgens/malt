from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.shortcuts import redirect

from base.views import BaseView

from bottle.models import Bottle
from glass.models import Glass, addDrinksInfo
from glass.forms import NewDrinkForm
from userprofile.models import UserProfile

class DrinksView(BaseView):
  template_name = "drinks/index.html"
  context_object_name = "drinks"
  
  def getAllDrinks(self):
    drinks = Glass.objects.order_by('-date')
    
    drinks = addDrinksInfo(drinks)
    return drinks
  
  def getMyDrinks(self, userProfileId):
    drinks = Glass.objects.filter(user__id=userProfileId).order_by('-date')
    
    drinks = addDrinksInfo(drinks)
    return drinks
  
  def get_context_data(self, **kwargs):
    context = super(DrinksView, self).get_context_data(**kwargs)
    bottles = self.getAllDrinks()
    context['all_drinks_list'] = bottles
    
    context['drinkssection'] = True
    return context


class MyDrinksView(DrinksView):
  template_name = "drinks/index.html"
  context_object_name = "drinks"
  
  def get_context_data(self, **kwargs):
    userProfile = UserProfile.objects.get(user=self.request.user)
    
    context = super(MyDrinksView, self).get_context_data(**kwargs)
    bottles = self.getMyDrinks(userProfile.id)
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
  
  
def plotDrinksVolumeHistory(request):
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
  canvas.print_png(response)
  
  return response

def newDrink(request):
  def errorHandle(error):
    kwargs = {'user' : request.user}
    form = NewDrinkForm(**kwargs)
    
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      context['drinkssection'] = True
    return render_to_response('drinks/new.html', context)
          
  if request.method == 'POST': # If the form has been submitted...
    kwargs = {'user' : request.user}
    form = NewDrinkForm(request.POST, **kwargs) # A form bound to the POST data
    
    if form.is_valid(): # All validation rules pass
      emptiesBottle = form.cleaned_data['emptiesBottle']
      if (emptiesBottle):
        bottle = form.cleaned_data['bottle']
        bottle.empty = True
        bottle.save()
        
      form.save()
      return redirect('/malt/drinks')
    else:
      error = u'form is invalid'
      return errorHandle(error)
  
  else:
    kwargs = {'user' : request.user}
    form = NewDrinkForm(**kwargs) # An unbound form
    form.fields["bottle"].queryset = Bottle.objects.filter(empty=False)
    context = RequestContext(request)
    context['form'] = form
    context['drinkssection'] = True
    
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      
    return render_to_response('drinks/new.html', context)
  
def newDrinkMobile(request):
  def errorHandle(error):
    kwargs = {'user' : request.user}
    form = NewDrinkForm(**kwargs)
    
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      context['drinkssection'] = True
    return render_to_response('drinks/newmobile.html', context)
          
  if request.method == 'POST': # If the form has been submitted...
    kwargs = {'user' : request.user}
    form = NewDrinkForm(request.POST, **kwargs) # A form bound to the POST data
    
    if form.is_valid(): # All validation rules pass
      emptiesBottle = form.cleaned_data['emptiesBottle']
      if (emptiesBottle):
        bottle = form.cleaned_data['bottle']
        bottle.empty = True
        bottle.save()
        
      form.save()
      return redirect('/malt/drinks')
    else:
      error = u'form is invalid'
      return errorHandle(error)
  
  else:
    kwargs = {'user' : request.user}
    form = NewDrinkForm(**kwargs) # An unbound form
    form.fields["bottle"].queryset = Bottle.objects.filter(empty=False)
    context = RequestContext(request)
    context['form'] = form
    context['drinkssection'] = True
    
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      
    return render_to_response('drinks/newmobile.html', context)