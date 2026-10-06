from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer, UserManageSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer


class UserManageView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserManageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
