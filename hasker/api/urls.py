from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from hasker.api import views

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'votes/', views.snippet_list)
]