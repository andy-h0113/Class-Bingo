from rest_framework import serializers
from BingoBackend.models import Board, Tile, User, BoardTile, BoardTileUser


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('board_id', 'board_name', 'dimension', 'active')


class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        fields = ('tile_id', 'text')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'password', 'num_wins')


class BoardTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardTile
        fields = ('tile_id', 'board_id')


class BoardTileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardTileUser
        fields = ('board_id', 'tile_id', 'user_id', 'position_row', 'position_col', 'selected')
