from django.urls import path

from .views import CreateNewsView, SearchNews, SortedLatest

urlpatterns = [
    path('create-news', CreateNewsView.as_view()),
    path('news/<str:query>/', SearchNews.as_view()),
    path('latest',SortedLatest.as_view())
]