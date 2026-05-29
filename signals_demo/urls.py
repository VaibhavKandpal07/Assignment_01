from django.urls import path
from . import views

urlpatterns = [
    path('q1/', views.test_q1_sync, name='q1_sync'),
    path('q2/', views.test_q2_thread, name='q2_thread'),
    path('q3/', views.test_q3_transaction, name='q3_transaction'),
]
