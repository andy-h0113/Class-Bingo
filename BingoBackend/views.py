from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import random

from rest_framework_simplejwt.views import TokenObtainPairView

from BingoBackend.models import Board, Tile, AppUser, BoardTile, BoardTileUser, Section
from BingoBackend.serializers import BoardSerializer, TileSerializer, UserSerializer, BoardTileSerializer, \
    BoardTileUserSerializer, SectionSerializer, RegisterSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import get_user_model, login, logout
from rest_framework.views import APIView
from rest_framework import status, authentication
from rest_framework.permissions import IsAuthenticated, AllowAny

UserModel = get_user_model()


class BoardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=0):
        if id:
            board = Board.objects.filter(board_id=id)
        else:
            board = Board.objects.all()
        board_serializer = BoardSerializer(board, many=True)
        return JsonResponse(board_serializer.data, safe=False)

    def post(self, request):
        board_data = JSONParser().parse(request)
        board_serializer = BoardSerializer(data=board_data)
        if board_serializer.is_valid():
            new_board = board_serializer.save()
            return JsonResponse({
                'board': new_board.board_id
            }, safe=False)
        else:
            print(board_serializer.errors)
        return JsonResponse("Failed to Add", status=status.HTTP_400_BAD_REQUEST, safe=False)

    def put(self, request):
        board_data = JSONParser().parse(request)
        board = Board.objects.get(board_id=board_data['board_id'])
        board_serializer = BoardSerializer(board, data=board_data)
        if board_serializer.is_valid():
            board_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)

    def delete(self, request, id):
        board = Board.objects.get(board_id=id)
        board.delete()
        return JsonResponse("Deleted Successfully", safe=False)


class TileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=0):
        tile = Tile.objects.all()
        tile_serializer = TileSerializer(tile, many=True)
        return JsonResponse(tile_serializer.data, safe=False)

    def post(self, request):
        tile_data = JSONParser().parse(request)
        tile_serializer = TileSerializer(data=tile_data)
        if tile_serializer.is_valid():
            tile_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)

    def put(self, request):
        tile_data = JSONParser().parse(request)
        tile = Tile.objects.get(tile_id=tile_data['tile_id'])
        tile_serializer = TileSerializer(tile, data=tile_data)
        if tile_serializer.is_valid():
            tile_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)

    def delete(self, request, id):
        tile = Tile.objects.get(tile_id=id)
        tile.delete()
        return JsonResponse("Deleted Successfully", safe=False)


class TileMultipleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tile_data = JSONParser().parse(request)
        for single_tile in tile_data["tiles"]:
            tile_serializer = TileSerializer(data=single_tile)
            if tile_serializer.is_valid():
                tile_serializer.save()
            else:
                return JsonResponse("Failed to Add", safe=False)
        return JsonResponse("Added Successfully", safe=False)


class SectionAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=0):
        if id:
            section = Section.objects.filter(section_id=id)
        else:
            section = Section.objects.all()
        section_serializer = SectionSerializer(section, many=True)
        return JsonResponse(section_serializer.data, safe=False)

    def post(self, request):
        section_data = JSONParser().parse(request)
        section_serializer = SectionSerializer(data=section_data)
        if section_serializer.is_valid():
            section_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)

    def delete(self, request, id=0):
        section = Section.objects.get(section_id=id)
        section.delete()
        return JsonResponse("Deleted Successfully", safe=False)


class BoardTileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id=0):
        if board_id:
            board_tile = BoardTile.objects.filter(board_id=board_id)
        else:
            board_tile = BoardTile.objects.all()
        board_tile_serializer = BoardTileSerializer(board_tile, many=True)
        return JsonResponse(board_tile_serializer.data, safe=False)

    def post(self, request):
        board_tile_data = JSONParser().parse(request)
        board_tile_serializer = BoardTileSerializer(data=board_tile_data)
        if board_tile_serializer.is_valid():
            board_tile_serializer.save()
            return JsonResponse("Added Successfully", safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(board_tile_serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        board_tile_data = JSONParser().parse(request)
        board_tile = BoardTile.objects.get(tile_id=board_tile_data['tile_id'])
        board_tile_serializer = BoardTileSerializer(board_tile, data=board_tile_data)
        if board_tile_serializer.is_valid():
            board_tile_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)

    def delete(self, request, board_id=0, tile_id=0):
        board_tile = BoardTile.objects.get(tile_id=tile_id, board_id=board_id)
        board_tile.delete()
        return JsonResponse("Deleted Successfully", safe=False)


class BoardTileUserApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id=0, user_id=0):
        # To get a single user board
        board_tile_user = BoardTileUser.objects.filter(board_id=board_id, user_id=user_id)
        board_tile_user_serializer = BoardTileUserSerializer(board_tile_user, many=True)
        return JsonResponse(board_tile_user_serializer.data, status=status.HTTP_200_OK, safe=False)

    def put(self, request, board_id=0, user_id=0):
        # Used to select or deselect a single tile
        board_tile_user_data = request.data
        board_tile_user = BoardTileUser.objects.get(user_id=board_tile_user_data['user'],
                                                    board_id=board_tile_user_data['board'],
                                                    tile_id=board_tile_user_data['tile'])
        board_tile_user_serializer = BoardTileUserSerializer(board_tile_user, data=board_tile_user_data)
        if board_tile_user_serializer.is_valid():
            board_tile_user_serializer.save()
            return JsonResponse("Updated Successfully", status=status.HTTP_200_OK, safe=False)
        return JsonResponse("Failed to Update", status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, board_id=0):
        # Used to delete all user boards of a specific board
        board_tile_user = BoardTileUser.objects.filter(board_id=board_id)
        board_tile_user.delete()
        return JsonResponse("Deleted Successfully", status=status.HTTP_200_OK, safe=False)


class PopulateUserBoardsNewBoard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id=0, section_id=0):
        all_board_tiles_options_QUERYSET = BoardTile.objects.filter(
            board=board_id)  # Gets all Tiles under this board
        all_section_users_QUERYSET = UserModel.objects.filter(
            section=section_id)  # Gets all Users under this section

        all_board_tiles_options = list(all_board_tiles_options_QUERYSET.values())
        all_section_users = list(all_section_users_QUERYSET.values())

        for user in all_section_users:
            user_tiles = random.sample(all_board_tiles_options, 25)
            bingo_board = [user_tiles[i:i + 5] for i in range(0, len(user_tiles), 5)]
            for x in range(0, len(bingo_board)):
                for y in range(0, len(bingo_board[x])):
                    board_tile_user = {
                        "user": user['user_id'],
                        "board": board_id,
                        "tile": bingo_board[x][y]['tile_id'],
                        "position_row": x,
                        "position_col": y,
                        "selected": False
                    }
                    board_tile_user_serializer = BoardTileUserSerializer(data=board_tile_user)
                    if board_tile_user_serializer.is_valid():
                        board_tile_user_serializer.save()
                    else:
                        return JsonResponse("Failed to create boards", status=status.HTTP_400_BAD_REQUEST, safe=False)
        return JsonResponse("Successfully Populated all Boards", status=status.HTTP_200_OK, safe=False)


class PopulateUserBoardsNewUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id=0):
        user = UserModel.objects.get(pk=user_id)
        user_data = UserSerializer(user, many=False).data
        all_boards_QUERYSET = Board.objects.filter(section=user.section_id)
        all_boards = list(all_boards_QUERYSET.values())


        for board in all_boards:
            all_board_tiles_options_QUERYSET = BoardTile.objects.filter(board=board['board_id'])  # Gets all Tiles under this board
            all_board_tiles_options = list(all_board_tiles_options_QUERYSET.values())

            if len(all_board_tiles_options) < 25:
                continue
            else:
                user_tiles = random.sample(all_board_tiles_options, 25)
                bingo_board = [user_tiles[i:i + 5] for i in range(0, len(user_tiles), 5)]

                for x in range(0, len(bingo_board)):
                    for y in range(0, len(bingo_board[x])):
                        board_tile_user = {
                            "user": user_data['user_id'],
                            "board": board['board_id'],
                            "tile": bingo_board[x][y]['tile_id'],
                            "position_row": x,
                            "position_col": y,
                            "selected": False
                        }
                        board_tile_user_serializer = BoardTileUserSerializer(data=board_tile_user)
                        if board_tile_user_serializer.is_valid():
                            board_tile_user_serializer.save()
                        else:
                            return JsonResponse("Failed to create board", status=status.HTTP_400_BAD_REQUEST, safe=False)
        return JsonResponse("Successfully populated new user boards", status=status.HTTP_200_OK, safe=False)


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        clean_data = request.data
        serializer = RegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                user_object = UserModel.objects.get(email=user.email)
                user_serializer = UserSerializer(user_object)
                return JsonResponse({'user': user_serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Failed to create user'}, status=status.HTTP_400_BAD_REQUEST)



class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=0):
        user = UserModel.objects.get(user_id=user_id)
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data, safe=False, status=status.HTTP_200_OK)

class UserSectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id=0):
        users = UserModel.objects.filter(section_id=section_id).order_by("num_wins").reverse()
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

