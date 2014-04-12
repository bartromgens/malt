from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from datetime import datetime

from django.http import HttpResponse 

from userprofile.forms import EditUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseUpdateView, BaseView
from glass.models import Glass, addDrinksInfo
from bottle.models import Bottle 


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
    
  def getTotalPaidNotDonated(self, userProfileId):
    bottles = Bottle.objects.filter(donation=False, buyer__id=userProfileId)
    
    totalPaid = 0.0
    
    for bottle in bottles:
      totalPaid += bottle.price
    
    return totalPaid
  
  def getTotalCostNotDonated(self, userProfileId):
    Bottle.objects.filter(donation=True, buyer__id=userProfileId)
    
    totalPaid = 0.0
    
    for bottle in bottles:
      totalPaid += bottle.price
    
    return totalPaid
  
  def get_context_data(self, **kwargs):
    userProfileId = kwargs['userProfileId']    
    context = super(StatsUserProfileView, self).get_context_data(**kwargs)
    
    totalVolume = 0.0
    totalCost = 0.0
    totalCostNotDonated = 0.0
    totalPaidNotDonated = self.getTotalPaidNotDonated(userProfileId)
    
    drinks = self.getUserDrinks(userProfileId)

    for drink in drinks:
      totalVolume += drink.volume
      cost = drink.bottle.price*drink.volume/drink.bottle.volume
      totalCost += cost
      if (not drink.bottle.donation):
        totalCostNotDonated += cost
      
    balance = totalPaidNotDonated - totalCostNotDonated
      
    nDrinks = drinks.count()
    if (nDrinks == 0):
      averageCost50ml = 0.0
    else:
      averageCost50ml = totalCost/totalVolume * 50
    
    context['drinks'] = drinks
    context['drinker'] = UserProfile.objects.get(id=userProfileId)
    context['volume_ml'] = '%.0f' % (totalVolume)
    context['total_cost'] = '%.2f' % (totalCost)
    context['average_cost_per_50ml'] = '%.2f' % (averageCost50ml)
    context['total_paid'] = '%.2f' % totalPaidNotDonated
    context['total_cost'] = '%.2f' % totalCostNotDonated
    context['balance'] = '%.2f' % balance
    
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


def plotRegionUserPieChart(request, userprofileId):
  fig = Figure()
  canvas = FigureCanvas(fig)
  ax = fig.add_axes([0,0,1,1])
  ax.axis('equal')

  #fig.suptitle('Regions')

  drinks = Glass.objects.filter(user_id=userprofileId)
  
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
