from rest_framework.serializers import ModelSerializer
from .models import User

import logging
logger = logging.getLogger(__name__)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
