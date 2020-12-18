from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="my_app-home"),
    path('new-search/',views.new_search,name="my_app-new_search"),
]