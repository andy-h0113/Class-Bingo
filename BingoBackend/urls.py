from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from BingoBackend import views

urlpatterns = [
    path('board/', views.BoardAPI.as_view(), name='board'),
    path('board/<int:id>/', views.BoardAPI.as_view(), name='board'),
    path('tile/', views.TileAPI.as_view(), name='tile'),
    path('tile/multiple/', views.TileMultipleAPI.as_view(), name='tile_multiple'),
    path('tile/<int:id>/', views.TileAPI.as_view(), name='tile'),
    path('section/', views.SectionAPI.as_view(), name='section'),
    path('section/<int:id>/', views.SectionAPI.as_view(), name='section'),
    path('boardtile/', views.BoardTileAPI.as_view(), name='board_tile'),
    path('boardtile/<int:board_id>/', views.BoardTileAPI.as_view(), name='board_tile'),
    path('boardtile/<int:board_id>/<int:tile_id>', views.BoardTileAPI.as_view(), name='board_tile'),
    path('boardtileuser/newboard/<int:board_id>/<int:section_id>/', views.PopulateUserBoardsNewBoard.as_view(), name='newboard'),
    path('boardtileuser/newuser/<int:user_id>/', views.PopulateUserBoardsNewUser.as_view(), name='newuser'),
    path('boardtileuser/<int:board_id>/<int:user_id>/', views.BoardTileUserApi.as_view(), name='board_tile_user'),
    path('boardtileuser/<int:board_id>/', views.BoardTileUserApi.as_view(), name='board_tile_user'),
    path('boardtileuser/', views.BoardTileUserApi.as_view(), name='board_tile_user'),
    path('user/<int:user_id>/', views.UserAPI.as_view(), name='user'),
    path('user/section/<int:section_id>/', views.UserSectionAPI.as_view(), name='user_section'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
]