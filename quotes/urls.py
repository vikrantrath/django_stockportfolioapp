from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('addStock.html', views.addStock, name="addStock"),
    path('deleteStock/<tickerName>', views.deleteStock, name="deleteStock"),    
]
