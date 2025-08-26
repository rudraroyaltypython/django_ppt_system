from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('presentation/<int:id>/', views.presentation_view, name='presentation'),
    path('impress/<int:id>/', views.impress_presentation_view, name='impress_presentation'),
]
