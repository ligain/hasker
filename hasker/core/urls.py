from django.urls import path
from hasker.core import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
]