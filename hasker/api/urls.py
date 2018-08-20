from django.conf.urls import include, url, re_path
from django.urls import path
from rest_framework.routers import DefaultRouter
from hasker.api import views

app_name = 'api1'

router = DefaultRouter()

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('votes/', views.VoteApiView.as_view()),
    path('right-answer/<int:pk>', views.RightAnswerUpdateApiView.as_view()),
    path('main-page/', views.MainPageApiView.as_view(), name='main-page'),
    path('trending/', views.TrendingApiView.as_view(), name='trending'),
    path('questions/<slug:slug>', views.QuestionApiView.as_view(), name='questions'),
    path('questions/<slug:slug>/answers', views.QuestionAnswersApiView.as_view(), name='answers-for-question'),
    path('search/tag/<slug:tag>', views.TagSearchApiView.as_view(), name='search-by-tag'),
    path('search/<str:q>', views.StringSearchApiView.as_view(), name='search-by-string')
]