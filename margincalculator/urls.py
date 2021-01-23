from django.urls import path
from . import views

urlpatterns = [
    path('options/', views.options, name="options"),
    path('options/calculate-margin', views.calculate_margin, name="calculate-margin"),
    path('calculator-entry/', views.calculator_entry, name="calculator-entry"),
]
