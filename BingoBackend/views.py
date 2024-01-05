from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from BingoBackend.models import Board, Tile, User, BoardTile, BoardTileUser
from BingoBackend.serializers import BoardSerializer, TileSerializer, UserSerializer, BoardTileSerializer, BoardTileUserSerializer


# Create your views here.
@csrf_exempt
def board_api(request, id=0):
    if request.method == 'GET':
        board = Board.objects.all()
        board_serializer = BoardSerializer(board, many=True)
        return JsonResponse(board_serializer.data, safe=False)
    elif request.method == 'POST':
        board_data = JSONParser().parse(request)
        board_serializer = BoardSerializer(data=board_data)
        if board_serializer.is_valid():
            board_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        board_data = JSONParser().parse(request)
        board = Board.objects.get(board_id=board_data['board_id'])
        board_serializer = BoardSerializer(board, data=board_data)
        if board_serializer.is_valid():
            board_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        board = Board.objects.get(board_id=id)
        board.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    return JsonResponse("Failed to Delete", safe=False)

@csrf_exempt
def tile_api(request, id=0):
    if request.method == 'GET':
        tile = Tile.objects.all()
        tile_serializer = TileSerializer(tile, many=True)
        return JsonResponse(tile_serializer.data, safe=False)
    elif request.method == 'POST':
        tile_data = JSONParser().parse(request)
        tile_serializer = TileSerializer(data=tile_data)
        if tile_serializer.is_valid():
            tile_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        tile_data = JSONParser().parse(request)
        tile = Tile.objects.get(tile_id=tile_data['tile_id'])
        tile_serializer = TileSerializer(tile, data=tile_data)
        if tile_serializer.is_valid():
            tile_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        tile = Tile.objects.get(tile_id=id)
        tile.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    return JsonResponse("Failed to Delete", safe=False)