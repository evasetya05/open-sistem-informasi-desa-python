from django.urls import path
from project import settings
from django.conf.urls.static import static

from dashboard.views import index

app_name = "dashboard"
urlpatterns = [
                  path('index/', index, name="index"),

              ]
