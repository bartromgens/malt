from django.template import RequestContext
from django.shortcuts import render_to_response

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
      form.save()
      context = RequestContext(request)

      if request.user.is_authenticated():
        context['user'] = request.user
        context['isLoggedin'] = True
        context['drinkssection'] = True

      return render_to_response('drinks/newsuccess.html', context)
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