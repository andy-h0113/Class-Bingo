
from django.contrib import admin

# Register your models here.
from .models import Section, Board, Tile, BoardTile, BoardTileUser
from django.contrib.auth.models import Group

admin.site.register(Section)
admin.site.register(Board)
admin.site.register(Tile)
admin.site.register(BoardTile)
admin.site.register(BoardTileUser)

admin.site.unregister(Group)

admin.site.site_header = "Class Bingo"