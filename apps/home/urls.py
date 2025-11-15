from django.urls import path
from .views import home, posting_investasi, detail_posting, create_posting_investasi

urlpatterns = [
    path('', home, name='home'),
    path('investasi/create/', create_posting_investasi, name='create_investasi'),
    path('investasi', posting_investasi, name='investasi'),
    path('investasi/<slug:slug>/', detail_posting, name='detail_posting'),
]
