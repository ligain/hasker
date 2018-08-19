from django.conf.urls import include, url, re_path
from django.urls import path
from rest_framework.routers import DefaultRouter
from hasker.api import views

router = DefaultRouter()

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('votes/', views.VoteApiView.as_view()),
    path('right-answer/<int:pk>', views.RightAnswerUpdateApiView.as_view()),
    path('main-page/', views.MainPageApiView.as_view()),
    path('trending/', views.TrendingApiView.as_view()),
    path('questions/<slug:slug>', views.QuestionApiView.as_view()),
    path('questions/<slug:slug>/answers', views.QuestionAnswersApiView.as_view()),
    path('search/tag/<slug:tag>', views.TagSearchApiView.as_view()),
    path('search/<str:q>', views.StringSearchApiView.as_view())
]