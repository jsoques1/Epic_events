from rest_framework.permissions import BasePermission
from .models import MGMT

import logging
logger = logging.getLogger(__name__)


class TestPermissions(BasePermission):
    def has_permission(self, request, view):
        print(f'request.user={request.user}')
        print(f'request.user.is_authenticated={request.user.is_authenticated}')
        # print(f'request.user.role={request.user.role}')
        # return request.user.role == MGMT
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == MGMT

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
