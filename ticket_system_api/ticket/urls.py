"""
Url mappings for ticket app.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ticket import views

router = DefaultRouter()
router.register('tickets', views.TicketViewSet)
router.register('comments', views.CommentViewSet)

app_name = 'ticket'

urlpatterns = [
    path('', include(router.urls)),
    path('metrics/', views.MetricView.as_view(), name='metrics'),
    path('employees/', views.EmployeesView.as_view(), name='employees')

]
