from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import EmailField, CharField, ValidationError
from rest_framework.validators import UniqueValidator
from .models import User

import logging
logger = logging.getLogger(__name__)


class UserSerializer(ModelSerializer):
    # email = EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    #
    password1 = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError({"Not matching passwords"})
        return data

    # def create(self, validated_data):
    #     user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
    #                                     first_name=validated_data['first_name'], last_name=validated_data['last_name'],
    #                                     password=validated_data['password'])
    #     user.save()
    #     return user
