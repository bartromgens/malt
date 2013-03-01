from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from datetime import datetime

from django.http import HttpResponse 

from userprofile.forms import EditUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseUpdateView, BaseView
from glass.models import Glass, addDrinksInfo


class UserProfilesView(BaseView):
  template_name = "userprofile/index.html"
  
  def get_context_data(self, **kwargs):    
    context = super(UserProfilesView, self).get_context_data(**kwargs)
    context['usersection'] = True
    
    context['userprofiles'] = UserProfile.objects.all().order_by('displayname')
    
    return context
  

class EditUserProfileView(BaseUpdateView):
  model = UserProfile
  form_class = EditUserProfileForm
  template_name = 'userprofile/edit.html'
    
  def get_context_data(self, **kwargs):
    context = super(EditUserProfileView, self).get_context_data(**kwargs)
    userProfile = UserProfile.objects.get(user=self.request.user)
    userProfileId = int(self.kwargs['pk'])
    
    # check whether user owns the UserProfile that is edited.
    if (userProfile.id == userProfileId):
      context['isAllowed'] = True;
    else:
      context.clear()    
      context['isAllowed'] = False;
    
    return context


class SuccessEditUserProfileView(BaseView):
  template_name = "userprofile/editsuccess.html"
  
  def get_context_data(self, **kwargs):    
    context = super(SuccessEditUserProfileView, self).get_context_data(**kwargs)
#    context['transactionssection'] = True
    
    return context
  
  
class StatsUserProfileView(BaseView):
  template_name = "userprofile/userstats.html"
  
  def getUserDrinks(self, userProfileId):
    drinks = Glass.objects.filter(user__id=userProfileId).order_by("bottle")
    drinks = addDrinksInfo(drinks)
    
    return drinks
  
  def get_context_data(self, **kwargs):
    userProfileId = kwargs['userProfileId']    
    context = super(StatsUserProfileView, self).get_context_data(**kwargs)
    
    drinks = self.getUserDrinks(userProfileId)
    totalVolume = 0.0
    totalCost = 0.0
    
    for drink in drinks:
      totalVolume += drink.volume
      totalCost += drink.bottle.price*drink.volume/drink.bottle.volume
      
    nDrinks = drinks.count()
    if (nDrinks == 0):
      averageCost = 0.0
    else:
      averageCost = totalCost/nDrinks

    volumeLiters = '%.0f' % (totalVolume)
    totalCostStr = '%.2f' % (totalCost)
    averageCostStr = '%.2f' % (averageCost)
    
    context['drinks'] = drinks
    context['drinker'] = UserProfile.objects.get(id=userProfileId)
    context['volume_ml'] = volumeLiters
    context['total_cost'] = totalCostStr
    context['average_cost_per_drink'] = averageCostStr
    
    context['usersection'] = True
    
    return context
  
  
def plotUserVolumeHistory(request, userprofileId):
  userprofile = UserProfile.objects.get(id=userprofileId)
  
  fig=Figure()
  canvas = FigureCanvas(fig)
  ax=fig.add_subplot(111)
  x=[]
  y=[]
  
  drinks = Glass.objects.filter(user=userprofile).order_by('date')
  
  fig.suptitle("Volume history " + str(userprofile.displayname))
  
  volume = 0.0
  
  x.append(userprofile.user.date_joined)
  y.append(volume)
  
  for drink in drinks:
    print drink.volume
    print drink.date
    x.append(drink.date)
    y.append(volume)
    volume += drink.volume
  
  x.append(datetime.now())
  y.append(volume)
  
  ax.step(x, y, '-', color='#106D2C')
  
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
