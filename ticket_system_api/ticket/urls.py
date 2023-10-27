"""
Url mappings for ticket app.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ticket import views

router = DefaultRouter()
router.register('tickets', views.TicketViewSet)

app_name = 'ticket'

urlpatterns = [
    path('', include(router.urls))
]
