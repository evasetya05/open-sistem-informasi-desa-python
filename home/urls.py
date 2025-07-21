from django.urls import path
from .views import home, posting_investasi, detail_posting

urlpatterns = [
    path('', home, name='home'),
    path('investasi', posting_investasi, name='investasi'),
    path('investasi/<slug:slug>/', detail_posting, name='detail_posting'),
]
