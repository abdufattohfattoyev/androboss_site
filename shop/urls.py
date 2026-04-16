from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('api/order/', views.order_submit, name='order_submit'),
    path('statistics/', views.statistics, name='statistics'),
]
