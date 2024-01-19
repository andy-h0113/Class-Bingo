from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from BingoBackend.models import Board, Tile, BoardTile, BoardTileUser, Section
from django.contrib.auth import get_user_model, authenticate


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('board_id', 'section', 'board_name', 'dimension', 'expiry_date', 'active')


class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        fields = ('tile_id', 'text')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('section_id', 'section_name')


class BoardTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardTile
        fields = ('board', 'tile')


class BoardTileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardTileUser
        fields = ('user', 'board', 'tile', 'position_row', 'position_col', 'selected')


UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('user_id', 'username', 'email', 'password', 'section_id', 'num_wins')

    def create(self, validated_data):
        user_obj = UserModel.objects.create_user(email=validated_data['email'], username=validated_data['username'],
                                                 section_id=validated_data['section_id'],
                                                 password=validated_data['password'])
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        user = authenticate(username=validated_data['email'], password=validated_data['password'])
        if not user:
            raise ValidationError('User not found')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('user_id', 'username', 'email', 'section_id', 'num_wins')