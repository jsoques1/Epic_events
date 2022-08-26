from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


from users.models import SALES, SUPPORT

import logging
logger = logging.getLogger(__name__)


class HasCustomerPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == SUPPORT:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == SALES

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'DELETE':
            return request.user.role == SALES
        else:
            return True


class HasContractPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == SUPPORT:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == SALES

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPPORT:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == SALES


class HasEventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == SUPPORT:
            return request.method in ['GET', 'PUT', 'DELETE']
        return request.user.role == SALES and request.method in ['GET', 'POST']

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' and obj.is_completed is True:
            raise PermissionDenied("The event has ended")
        elif request.method == 'DELETE' and obj.is_completed is False:
            raise PermissionDenied("The event has not ended")
        return True
