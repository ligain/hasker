from django.urls import path
from hasker.profiles import views
from django.contrib.auth import views as auth_views


app_name = 'profiles'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
]