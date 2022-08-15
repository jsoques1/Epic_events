from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from .permissions import IsManager
from .models import User
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

import logging
logger = logging.getLogger(__name__)


# class UserCreateView(CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated, IsManager,)
#     serializer_class = UserSerializer
#
#     print('In UserCreateView')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer, *args, **kwargs):
        request_data = serializer.data
        user = User.objects.get(username=request_data['username'])
        if user:
            raise ValidationError(f'A user {request_data["username"]} already exists')

        serializer = UserSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    # def perform_update(self, serializer, *args, **kwargs):
    #     request_data = self.request.data
    #     author_user = User.objects.get(id=request_data['author_user'])
    #     if int(self.request.user.id) != int(author_user.id):
    #         raise ValidationError('Requesting user should equal to author_user')
    #
    #     comment = self.get_object()
    #     if int(self.request.user.id) != int(comment.author_user_id):
    #         raise ValidationError('Requesting user {self.request.user.username} is not the project author')
    #
    #     instance = self.get_object()  # instance before update
    #     updated_instance = serializer.save()
    #
    # def destroy(self, request, *args, **kwargs):
    #     project_id = self.kwargs['pk']
    #     authors = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
    #     if not authors:
    #         raise ValidationError('Requesting user should be the project author')
    #
    #     project = self.get_object()
    #     project.delete()
    #     return Response({'message': 'Project deleted'}, status=status.HTTP_200_OK)