from django.urls import path
from hasker.profiles import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
]