import random

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from .models import Sticker, User

from .serializers import StickerSerializer


class StickerViewSet(viewsets.ViewSet):
    def list(self, request):
        stickers = Sticker.objects.all()
        serializer = StickerSerializer(stickers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StickerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            sticker = Sticker.objects.get(id=pk)
            serializer = StickerSerializer(sticker)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("Not Found", status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            sticker = Sticker.objects.get(id=pk)
            serializer = StickerSerializer(instance=sticker, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response("Not Found", status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            sticker = Sticker.objects.get(id=pk)
            sticker.delete()
            return Response("Deleted", status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Not Found", status.HTTP_404_NOT_FOUND)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
