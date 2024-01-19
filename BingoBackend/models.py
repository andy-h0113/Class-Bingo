from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from ClassBingo import settings


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100)


class Tile(models.Model):
    tile_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    board_name = models.CharField(max_length=20)
    dimension = models.IntegerField(default=5)
    active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(default=False)


class BoardTile(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['board_id', 'tile_id'], name='unique_board_tile_combination'
            )
        ]


class AppUserManager(BaseUserManager):
    def create_user(self, email, username, section_id, password=None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("A password is required")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            section_id=section_id,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, section_id, password=None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("A password is required")
        user = self.create_user(email, username, section_id, password)
        user.is_superuser = True
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    num_wins = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'section_id']
    objects = AppUserManager()


class BoardTileUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE)
    position_row = models.IntegerField()
    position_col = models.IntegerField()
    selected = models.BooleanField(default=False)