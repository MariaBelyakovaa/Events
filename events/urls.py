from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/participate/', views.participate, name='participate'),
    path('event/<int:event_id>/comment/', views.add_comment, name='add_comment'),
]