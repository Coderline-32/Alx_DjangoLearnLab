from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser

# Create your views here.

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "username": user.username})


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, pk, *args, **kwargs):
        user_to_follow = get_object_or_404(CustomUser, pk=pk)
        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"success": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, pk, *args, **kwargs):
        user_to_unfollow = get_object_or_404(CustomUser, pk=pk)
        if user_to_unfollow == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"success": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)


