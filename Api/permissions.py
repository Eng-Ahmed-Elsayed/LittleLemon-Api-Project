from rest_framework import permissions

# Check if the user is in manager group
def isManager(request):
    if request.user.groups.filter(name='Manager').exists():
        return True
    return False

# Check if the user is Delivery crew group
def isDelivery(request):
    if request.user.groups.filter(name='Delivery crew').exists():
        return True
    return False

# Check if the user has no groups
def isCustomer(request):
    if len(request.user.groups.all()) == 0:
        return True
    return False

# Permission for super user and Manager.
class IsManagerOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if isManager(request):
                return True

# Permission for Customers (has 0 groups).
class IsAndOnlyCustomerGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if isCustomer(request):
                return True