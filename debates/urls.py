from django.urls import path
from .views import *


urlpatterns = [
    path("create", DebateCreateAPIView.as_view()),
    path("raffle", RandomDebateApplyView.as_view()),
]