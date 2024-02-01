from django.urls import path
from .views import *


urlpatterns = [
    path("list", PetitionListAPIView.as_view()),
    path("detail", PetitionDetailAPIView.as_view()),
]