from django.urls import path
from hasker.core import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('ask/', views.CreateQuestionView.as_view(), name='ask'),
    path('question/<slug:slug>', views.QuestionView.as_view(), name='question'),
    path('vote/', views.update_vote, name='vote'),
]
