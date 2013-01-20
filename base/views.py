from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.views.generic.edit import UpdateView
from itertools import chain
from base.forms import LoginForm, UserCreateForm
from bottle.models import Bottle
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
    user = self.request.user
    
    from bottle.views import CollectionView
    collectionView = CollectionView()
    
    totalInStock_L = Bottle.getActualVolumeAll(Bottle())
    totalActualValue = Bottle.getActualValueAll(Bottle())
      
    totalInStock_L_str = '%.1f' % totalInStock_L
    
    bottlesList = CollectionView.getOverviewBottleLists(collectionView)
    context['stock_lists'] = bottlesList 
    context['totalInStock_L'] = totalInStock_L_str 
    context['total_actual_value'] = totalActualValue 
    context['value_per_liter'] = totalActualValue / totalInStock_L
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
          
        
def register(request):
  def errorHandle(error):
    form = UserCreateForm()
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    return render_to_response('base/register.html', context)
    
  if request.method == 'POST': # If the form has been submitted...
    form = UserCreateForm(request.POST) # A form bound to the POST data
    if form.is_valid():
      form.save()
      context = RequestContext(request)
      context['registered'] = True
      return render_to_response('base/register.html', context)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  else:
    form = UserCreateForm() # An unbound form
    context = RequestContext(request)
    context['form'] = form
    return render_to_response('base/register.html', context)

        
def login(request):
  def errorHandle(error):
    form = LoginForm()
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    return render_to_response('base/login.html', context)
        
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
          context = RequestContext(request)
          context['user'] = user
          context['isLoggedin'] = True
          return render_to_response('base/index.html', context)
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
    form = LoginForm() # An unbound form
    context = RequestContext(request)
    context['form'] = form
    return render_to_response('base/login.html', context)

    
def logout(request):
  auth.logout(request)
  context = RequestContext(request)
  return render_to_response('base/index.html', context)