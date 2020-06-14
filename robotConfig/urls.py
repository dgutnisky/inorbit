from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<str:robot_id>/', views.showRobot, name='showRobot'),
    path('<str:robot_id>/update', views.updateRobot, name='updateRobot')
]