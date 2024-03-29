from django.urls import path
from .views import *


urlpatterns = [
    path("create", DebateCreateAPIView.as_view()),
    path("raffle", RandomDebateApplyView.as_view()),
    path("apply", UserDebateAPIView.as_view()),
    path("statement", DebateStatementAPIView.as_view()),
    path("summary", StatementSummaryAPIView.as_view()),
]