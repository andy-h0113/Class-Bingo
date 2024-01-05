from django.urls import path
from BingoBackend import views

urlpatterns = [
    path('board/', views.board_api),
    path('board/<int:id>/', views.board_api),
    path('tile/', views.board_api),
    path('tile/<int:id>/', views.board_api),

]