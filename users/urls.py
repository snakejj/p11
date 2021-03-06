from django.urls import path, include

from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.account_activation, name='activate'),
]

