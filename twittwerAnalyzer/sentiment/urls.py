from django.urls import path

from . import views

app_name = 'sentiment'

urlpatterns = [
    path('', views.index, name='index'),
    # /sentiment/detail
    #path('<int:tweet_id>/', views.detail, name='detail'),
    # /sentiment/results
    #path('<int:tweet_id>/results/', views.results, name='results'),
]