from django.urls import path

from utm import views

app_name = 'utm'
urlpatterns = [
    path('check_utm/', views.check_utm, name='check_utm'),
]