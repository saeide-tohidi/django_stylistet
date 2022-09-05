from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets, permissions, generics
from account.models import UserProfile, User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from account.api.serializers import (
    UserRegisterSerializer,
    ChangePasswordSerializer,
)


class UserRegisterAPIViewSet(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(
                email=request.data["email"], username=request.data["username"]
            ).exists():
                return Response(
                    data="This email or username does exist so try another",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User(email=request.data["email"], username=request.data["username"])
            password = request.data["password"]
            re_password = request.data["re_password"]

            if password != re_password:
                return Response(
                    data="Two pass should be same!", status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(password)
            user.save()
            token = Token.objects.get(user=user)
            data = {"user": user.email, "token": token.key}
            return Response(data, status=status.HTTP_201_CREATED)


class UpdatePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(data="Password changed", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data="You logged out", status=status.HTTP_200_OK)
