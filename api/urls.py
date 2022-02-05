from django.urls import path

from .views import CreateNewsView

urlpatterns = [
    path('create-news', CreateNewsView.as_view()),
]