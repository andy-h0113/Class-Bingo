from django.db import models


# Global Constants
# MAX_DIMENSION = 8
# MIN_DIMENSION = 1
# position_row = models.IntegerField(
#         validators=[
#             MaxValueValidator(MAX_DIMENSION),
#             MinValueValidator(MIN_DIMENSION)
#         ])
# from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    num_wins = models.IntegerField(default=0)


class Tile(models.Model):
    tile_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    board_name = models.CharField(max_length=20)
    dimension = models.IntegerField()
    active = models.BooleanField(default=True)


class BoardTile (models.Model):
    tile_id = models.ForeignKey(Tile, on_delete=models.CASCADE)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)


class BoardTileUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    tile_id = models.ForeignKey(Tile, on_delete=models.CASCADE)
    position_row = models.IntegerField()
    position_col = models.IntegerField()
    selected = models.BooleanField(default=False)
