from django.urls import path
from .views import HomepageView, DetailReportView

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    path("current-weather/", DetailReportView.as_view(), name="detail_report"),
]
