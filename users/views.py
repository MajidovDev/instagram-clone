from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shared_app.utility import send_email
from users.models import UserModel, DONE, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE
from users.serializers import SignUpSerializer, ChangeUserInfoSerializer, ChangeUserPhotoSerializer, LoginSerializer, \
    LoginRefreshSerializer


class CreateUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(),code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Tadiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerification(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.phone_number, code)
        else:
            data = {
                "message": "Email or Phone Number is incorrect"
            }
            raise ValidationError(data)
        return Response(
            {
                "success": True,
                "message": "Your confirmation code resent"
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Kodingiz ishlatishga yaroqli, Biroz kutib turing"
            }
            raise ValidationError(data)


class ChangeUserInfoView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInfoSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInfoView, self).update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "User updated successfully",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=200)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInfoView, self).partial_update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "User partially updated successfully",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=200)


class ChangeUserPhotoView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response(
                {
                    "message": "Photo updated successfully"
                },
                status=200
            )
        return Response(
            serializer.errors, status=400
        )


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer