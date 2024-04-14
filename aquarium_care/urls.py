from django.urls import path
from .views import * 

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-aquarium/', CreateAquariumView.as_view(), name='create_aquarium'),
    path('interaction/<int:aquarium_id>', InteractionView.as_view(), name='interaction'),
    path('profile/<int:profile_id>', ProfileView.as_view(), name='profile'),
    path('accounts/authorization/', AuthorizationView.as_view(), name='auth'),
    path('accounts/registration/', RegistrationView.as_view(), name='reg'),
    path('pincode-login/<int:auquarium_id>/', PincodeLoginView.as_view(), name='pincode_login'),
    path('message/<int:message_id>/', MessageView.as_view(), name='message'),
    path('statistic/<int:statistic_id>/', StatisticView.as_view(), name='statistic'),
    path('reset/', ResetView.as_view(), name='reset'),
    path('sell_fish/<int:fish_id>/', SellFishView.as_view(), name='sell_fish'),
    path('sell_shrimp/<int:shrimp_id>/', SellShrimpView.as_view(), name='sell_shrimp'),
    path('sell_snail/<int:snail_id>/', SellSnailView.as_view(), name='sell_snail'),
    path('sell_fugue/<int:fugue_id>/', SellFugueView.as_view(), name='sell_fugue'),
    
    path('fishes/', FishListView.as_view(), name='fish_list'),
]
