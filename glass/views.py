from base.views import BaseView

from glass.models import Glass
from userprofile.models import UserProfile

class DrinksView(BaseView):
  template_name = "drinks/index.html"
  context_object_name = "transaction"
  
  def addDrinkInfo(self, drinks):
    for drink in drinks:
      drink.price = '%.2f' % drink.getPrice()
      
    return drinks
  
  def getAllDrinks(self):
    drinks = Glass.objects.order_by("date")
    
    drinks = self.addDrinkInfo(drinks)
    return drinks
  
  def getMyDrinks(self, userProfileId):
    drinks = Glass.objects.filter(user__id=userProfileId).order_by("date")
    
    drinks = self.addDrinkInfo(drinks)
    return drinks
  
  def get_context_data(self, **kwargs):
    context = super(DrinksView, self).get_context_data(**kwargs)
    bottles = self.getAllDrinks()
    context['all_drinks_list'] = bottles
    
    context['drinkssection'] = True
    return context


class MyDrinksView(DrinksView):
  template_name = "drinks/index.html"
  context_object_name = "transaction"
  
  def get_context_data(self, **kwargs):
    userProfile = UserProfile.objects.get(user=self.request.user)
    
    context = super(MyDrinksView, self).get_context_data(**kwargs)
    bottles = self.getMyDrinks(userProfile.id)
    context['all_drinks_list'] = bottles
    
    context['drinkssection'] = True
    return context
  