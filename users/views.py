from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from users.models import UserModel
from users.serializers import SignUpSerializer


class CreateUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer