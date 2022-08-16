from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Customer, Contract


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
            return request.user.role == SALES and obj.is_client is False
        elif request.user.role == SUPPORT and request.method in permissions.SAFE_METHODS:
            return obj in Customer.objects.filter(contract__event__support=request.user)
        return request.user == obj.salesman or obj.is_client is False


class HasContractPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == SUPPORT:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == SALES

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user.role == SUPPORT:
                return obj in Contract.objects.filter(event__support=request.user)
            return request.user == obj.sales_contact
        elif request.method == 'PUT' and obj.is_signed is True:
            raise PermissionDenied("The contract is already signed")
        return request.user == obj.salesman and obj.is_signed is False


class HasEventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.team == SUPPORT:
            return request.method in ['GET', 'PUT']
        return request.user.role == SALES

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.support or request.user == obj.contract.salesman
        else:
            if obj.event_status is True:
                raise PermissionDenied("Cannot update a finished event.")
            if request.user.role == SUPPORT:
                return request.user == obj.support
            return request.user == obj.contract.salesman
