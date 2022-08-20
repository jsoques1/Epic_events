from rest_framework.permissions import BasePermission
from .models import MGMT

import logging
logger = logging.getLogger(__name__)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == MGMT

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
