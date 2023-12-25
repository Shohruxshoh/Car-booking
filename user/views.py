from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from booking.serializers import CompanySerializer
from carBooking.permissions import IsOwnerOrReadOnly
from user.models import User, Job, Company
from user.serializers import UserSerializer, MyTokenObtainPairSerializer, CustomTokenRefreshSerializer, \
    LogoutSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserGetSerializer, JObSerializer
from user.utils import equal_username_view


# Create your views here.

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        if equal_username_view(user.username, new_password):
            user.set_password(new_password)
            user.save()

            refresh = user.tokens()
            try:
                refresh_token = refresh['refresh']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            except TokenError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'detail': 'Parol kamida 8 ta belgidan iborat, kichik, bosh harflar va belgilardan tashkil topgan bo’lishi kerak. Kamida 2 ta bosh harf albatta bo’lishi kerak va username bilan parol bir xil bo\'lmasin'},
                status=status.HTTP_400_BAD_REQUEST)


class UserApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.user.username).first()
        serializer = UserGetSerializer(user)
        return Response(serializer.data)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserResetPasswordView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(id=pk).first()
        new_password = serializer.validated_data['new_password']
        if equal_username_view(user.username, new_password):
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail': 'Parol kamida 8 ta belgidan iborat, kichik, bosh harflar va belgilardan tashkil topgan bo’lishi kerak. Kamida 2 ta bosh harf albatta bo’lishi kerak va username bilan parol bir xil bo\'lmasin'},
                status=status.HTTP_400_BAD_REQUEST)


class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JObSerializer
    permission_classes = (IsAuthenticated,)


class JobListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JObSerializer
    permission_classes = (IsAuthenticated,)


class JobUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JObSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)


class CompanyCreateListView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)


class CompanyUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
