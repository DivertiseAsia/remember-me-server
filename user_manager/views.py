from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from user_manager.serializers import UserSerializer, RegistrationSerializer, LoginSerializer, BirthdaySerializer, \
    ChangePasswordSerializer

account_activation_token = PasswordResetTokenGenerator()


class AccountViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    User = get_user_model()
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False, serializer_class=RegistrationSerializer, permission_classes=(AllowAny,))
    def register(self, request):
        """
        New user registration.
        ---
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, serializer_class=LoginSerializer, permission_classes=(AllowAny,))
    def login(self, request):
        """
        Active user signing in.
        ---
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.verify_user()
            if not user:
                return Response({'error': {'password': ['Password is wrong.']}}, status=status.HTTP_400_BAD_REQUEST)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, serializer_class=UserSerializer)
    def profile(self, request):
        """
        Retrieve user profile.
        ---
        """
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, serializer_class=BirthdaySerializer)
    def birthday(self, request):
        """
        Get all active user birth dates.
        ---
        """
        queryset = self.get_queryset().filter(user__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    User = get_user_model()
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False, serializer_class=ChangePasswordSerializer)
    def change(self, request):
        """
        Authorized user changes password.
        ---
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'error': {'old_password': ['Password is wrong.']}}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
