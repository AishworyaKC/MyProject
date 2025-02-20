from django.urls import path
from .views import register, login, user_profile, activate_membership

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', user_profile, name='user_profile'),
    path('activate-membership/', activate_membership, name='activate_membership'),
]
