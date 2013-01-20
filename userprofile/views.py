from userprofile.forms import EditUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseUpdateView, BaseView
from glass.models import Glass, addDrinksInfo

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
      
    volumeLiters = '%.0f' % (totalVolume)
    totalCostStr = '%.2f' % (totalCost)
    averageCostStr = '%.2f' % (totalCost/drinks.count())
    
    context['drinks'] = drinks
    context['drinker'] = UserProfile.objects.get(id=userProfileId)
    context['volume_ml'] = volumeLiters
    context['total_cost'] = totalCostStr
    context['average_cost_per_drink'] = averageCostStr
    
    return context