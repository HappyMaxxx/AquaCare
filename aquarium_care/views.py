from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from .models import *
from django.core import serializers
from django.http import JsonResponse

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .forms import *

import time
from threading import Thread

def timer(aquarium_id):
    aquarium = Aquarium.objects.get(pk=aquarium_id)
    fishes = Fish.objects.filter(aquarium = aquarium)
    shrimps = Shrimp.objects.filter(aquarium=aquarium)
    snails = Snail.objects.filter(aquarium=aquarium)
    fugues = Fugue.objects.filter(aquarium=aquarium)
    while True:
        time.sleep(5)
        for fish in fishes:
            if fish.is_alive:
                fish.satiety -= 10
                if fish.satiety == 0:
                    fish.is_alive = False
                fish.save()
        for shrimp in shrimps:
            if shrimp.is_alive:
                shrimp.satiety -= 10
                if shrimp.satiety == 0:
                    shrimp.is_alive = False
                shrimp.save()
        for snail in snails:
            if snail.is_alive:
                snail.satiety -= 10
                if snail.satiety == 0:
                    snail.is_alive = False
                snail.save()
        for fugue in fugues:
            if fugue.is_alive:
                fugue.satiety -= 10
                if fugue.satiety == 0:
                    fugue.is_alive = False
                fugue.save()
        if aquarium.pollution > 0:
            aquarium.pollution -= 4
            aquarium.save()
        else:
            aquarium.pollution = 0
            aquarium.save()
        
        
class PincodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/profile/'):
            if 'pincode' not in request.session or not request.session['pincode']:
                aquarium_id = request.path.split('/')[2]
                return redirect(reverse('pincode_login', args=[aquarium_id]))

        response = self.get_response(request)
        return response

class IndexView(TemplateView):      
    template_name = 'aquarium_care/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class LoginRequiredMixin(AccessMixin):
    login_url = reverse_lazy('auth')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class IsAuthenticatedMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated
    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())

class RegistrationView(IsAuthenticatedMixin, CreateView): 
    template_name = 'aquarium_care/reg.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('auth')
    login_url = '/'
    
class AuthorizationView(IsAuthenticatedMixin, LoginView):
    form_class = CustomLoginForm
    template_name = 'aquarium_care/auth.html'
    login_url = '/'
    
class CreateAquariumView(LoginRequiredMixin, TemplateView):
    template_name = 'aquarium_care/create_aquarium.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def post(self, request, *args, **kwargs):
        aquarium = Aquarium.objects.create(owner=request.user, pincode=request.POST['pincode'])

        for _ in range(int(request.POST['fish'])):
            Fish.objects.create(aquarium=aquarium, gender=random.choice([True, False]), time_of_birth=datetime.datetime.now())  
        for _ in range(int(request.POST['shrimp'])):
            Shrimp.objects.create(aquarium=aquarium, gender=random.choice([True, False]), time_of_birth=datetime.datetime.now())
        for _ in range(int(request.POST['snail'])):
            Snail.objects.create(aquarium=aquarium, gender=random.choice([True, False]), time_of_birth=datetime.datetime.now())
        for _ in range(int(request.POST['fugue'])):
            Fugue.objects.create(aquarium=aquarium, gender=random.choice([True, False]), time_of_birth=datetime.datetime.now())
        return redirect('interaction', aquarium_id=aquarium.id)


class InteractionView(TemplateView): 
    template_name = 'aquarium_care/interaction.html'
    def get_context_data(self, **kwargs):
        background_thread = Thread(target=timer, args=(self.kwargs['aquarium_id'],))
        background_thread.start() 
        context = super().get_context_data(**kwargs)
        context['aquarium'] = Aquarium.objects.get(pk=self.kwargs['aquarium_id'])
        return context

class ProfileView(TemplateView):
    template_name = 'aquarium_care/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aquarium'] = Aquarium.objects.get(pk=self.kwargs['profile_id'])
        context['fishes'] = len(Fish.objects.filter(aquarium=context['aquarium']))
        context['shrimps'] = len(Shrimp.objects.filter(aquarium=context['aquarium']))
        context['snails'] = len(Snail.objects.filter(aquarium=context['aquarium']))
        context['fugues'] = len(Fugue.objects.filter(aquarium=context['aquarium']))
        context['notification'] = []
        fishes = Fish.objects.all()
        for fish in fishes:
            if fish.satiety < 20:
                context['notification'].append(f'Критичний рівень голоду риби {fish.id}.')
            if not fish.is_alive:
                context['notification'].append(f'Риба {fish.id} померла.')
        shrimps = Shrimp.objects.all()
        for shrimp in shrimps:
            if shrimp.satiety < 20:
                context['notification'].append(f'Критичний рівень голоду креветки {shrimp.id}.')
            if not shrimp.is_alive:
                context['notification'].append(f'Креветка {shrimp.id} померла.')
        snails = Snail.objects.all()
        for snail in snails:
            if snail.satiety < 20:
                context['notification'].append(f'Критичний рівень голоду равлика {snail.id}.')
            if not snail.is_alive:
                context['notification'].append(f'Равлик {snail.id} помер.')
        fugues = Fugue.objects.all()
        for fugue in fugues:
            if fugue.satiety < 20:
                context['notification'].append(f'Критичний рівень голоду фуги {fugue.id}.')
            if not fugue.is_alive:
                context['notification'].append(f'Фугу {fugue.id} помер.')
        if context['aquarium'].pollution < 20:
            context['notification'].append('Потрібно прибрати акваріум')
        return context
    def get(self, request, *args, **kwargs):
        self.request.session['pincode'] = None
        return super().get(request, *args, **kwargs)

class PincodeLoginView(View):
    form_class = PincodeForm
    template_name = 'aquarium_care/pincode.html'
    
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print('User is not authenticated')
            return redirect('auth')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pincode_input = form.cleaned_data['pincode']
            
            pincode = Aquarium.objects.get(pk=self.kwargs['auquarium_id'] ).pincode
            if int(pincode_input) == pincode:
                request.session['pincode'] = True
                return redirect('profile', profile_id=self.kwargs['auquarium_id'])
        return render(request, self.template_name, {'form': form})

class MessageView(View):
    template_name = 'aquarium_care/messages.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['idg'] = self.kwargs['message_id']
        context['aquarium'] = Aquarium.objects.get(pk=self.kwargs['profile_id'])
        context['fishes'] = len(Fish.objects.filter(aquarium=context['aquarium']))
        context['shrimps'] = len(Shrimp.objects.filter(aquarium=context['aquarium']))
        context['snails'] = len(Snail.objects.filter(aquarium=context['aquarium']))
        context['fugues'] = len(Fugue.objects.filter(aquarium=context['aquarium']))
        context['notification'] = []
        print("okey")

        return context
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# class StatisticView(View):
#     template_name = 'aquarium_care/statistic.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         fishes=Fish.objects.filter(self.kwargs['statistic_id'])
#         context['fishes'] = fishes

#         return context
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

class StatisticView(TemplateView):
    template_name = 'aquarium_care/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistic_id = self.kwargs['statistic_id']
        aquarium = Aquarium.objects.get(pk=statistic_id)
        fishes = Fish.objects.filter(aquarium=aquarium, is_alive=True)
        shrimps = Shrimp.objects.filter(aquarium=aquarium, is_alive=True)
        snails = Snail.objects.filter(aquarium=aquarium, is_alive=True)
        fugues = Fugue.objects.filter(aquarium=aquarium, is_alive=True)
        context['fishes'] = fishes
        context['shrimps'] = shrimps
        context['snails'] = snails
        context['fugues'] = fugues
        context['balance'] = aquarium.money
        return context
    
class ResetView(View):
    def get(self, request, *args, **kwargs):
        request.session['pincode'] = None
        logout(request)
        return redirect('index')
    
class FishListView(View):
    def get(self, request):
        fishes = list(Fish.objects.values('id', 'satiety'))
        shrimps = list(Shrimp.objects.values('id', 'satiety'))
        snails = list(Snail.objects.values('id', 'satiety'))
        fugues = list(Fugue.objects.values('id', 'satiety'))

        all_organic = {
            'fishes': fishes,
            'shrimps': shrimps,
            'snails': snails,
            'fugues': fugues,
        }
        return JsonResponse(all_organic)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class SellFishView(View):
    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    def post(self, request, *args, **kwargs):
        fish = Fish.objects.get(pk=self.kwargs['fish_id'])
        fish.is_sold = True
        fish.aquarium.money += fish.cost  
        fish.aquarium.save()
        fish.save()
        return redirect('statistic', statistic_id=fish.aquarium.id)

class SellShrimpView(View):
    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    def post(self, request, *args, **kwargs):
        shrimp = Shrimp.objects.get(pk=self.kwargs['shrimp_id'])
        shrimp.is_sold = True
        shrimp.aquarium.money += shrimp.cost  
        shrimp.aquarium.save()
        shrimp.save()
        return redirect('statistic', statistic_id=shrimp.aquarium.id)

class SellSnailView(View):
    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    def post(self, request, *args, **kwargs):
        snail = Snail.objects.get(pk=self.kwargs['snail_id'])
        snail.is_sold = True
        snail.aquarium.money += snail.cost  
        snail.aquarium.save()
        snail.save()
        return redirect('statistic', statistic_id=snail.aquarium.id)

class SellFugueView(View):
    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    def post(self, request, *args, **kwargs):
        fugue = Fugue.objects.get(pk=self.kwargs['fugue_id'])
        fugue.is_sold = True
        fugue.aquarium.money += fugue.cost  
        fugue.aquarium.save()
        fugue.save()
        return redirect('statistic', statistic_id=fugue.aquarium.id)

def my_view(request):
            referer = request.META.get('HTTP_REFERER')
            return render(request, 'my_template.html', {'referer': referer})