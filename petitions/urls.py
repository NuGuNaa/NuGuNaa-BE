from django.urls import path
from .views import *


urlpatterns = [
    path("list", PetitionListAPIView.as_view()),
]