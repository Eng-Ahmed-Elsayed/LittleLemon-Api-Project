from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
# We will use TokenAuthentication only use SessionAuthentication to debugging
# , SessionAuthentication
# use the default setting so don't need to import this again. Do it if you will change throttling setting and if u will use custom throttling
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.shortcuts import get_object_or_404

from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, DeliveryOrderSerializer, OrderItemSerializer, ManagerOrderSerializer, UserGroupsSerializers
from .permissions import IsManagerOrSuperUser, IsAndOnlyCustomerGroup, isManager, isDelivery, isCustomer
# Create your views here.

# Model view for category only admins can use
class CategoriesModelView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['title']

# Model view for MenuItem only managers can use all avalible methods
# Customers can use only list and retrieve
class MenuItemModelView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'featured']
    filterset_fields = ['title', 'price', 'featured'] 
    search_fields = ['title', 'price', 'featured']
    
    # manage permissions
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManagerOrSuperUser]
        return [permission() for permission in permission_classes]

# View for managers to list all the users that have manager group
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsManagerOrSuperUser])
def ManagersListView(request):
    if request.method == 'GET':
        managers = User.objects.filter(groups__name='Manager')
        serializer = UserGroupsSerializers(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# View for managers to add or delete user from manager group
@api_view(['POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsManagerOrSuperUser])
def ManagersCreateDeleteView(request, pk):
    managerGroup = Group.objects.get(name="Manager")
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        managerGroup.user_set.add(user)
        return Response({'message': 'Created'}, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        managerGroup.user_set.remove(user)
        return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)
    else:
        return Response({"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# View for managers to list all the users that have delivery crew group
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsManagerOrSuperUser])
def DeliveryCrewListView(request):
    if request.method == 'GET':
        deliveryCrew = User.objects.filter(groups__name='Delivery crew')
        serializer = UserGroupsSerializers(deliveryCrew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# View for managers to add or delete user from delivery crew group
@api_view(['POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsManagerOrSuperUser])
def DeliveryCrewCreateDeleteView(request, pk):
    deliveryCrewGroup = Group.objects.get(name="Delivery crew")
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        deliveryCrewGroup.user_set.add(user)
        return Response({'message': 'Created'}, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        deliveryCrewGroup.user_set.remove(user)
        return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)
    else:
        return Response({"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# Model view to manage items in the cart
class CartModelView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAndOnlyCustomerGroup]

    # List all cart objects for this user
    def list(self, request):
        userCart = Cart.objects.filter(user=request.user)
        serializer = self.get_serializer(userCart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create new cart object
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            menuItem = MenuItem.objects.get(pk=serializer.data.get('menuItem'))
            cart = Cart(
                user = request.user,
                menuItem = menuItem,
                quantity = serializer.data.get('quantity'),
                unit_price = serializer.data.get('unit_price'),
                price = serializer.data.get('price')
            )
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "UNIQUE constraint failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Delete all cart objects for this user
    def destroy(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# Model view to manage the Orders
class OrdersModelView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Manager
        if isManager(request) or request.user.is_superuser:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Delivery crew
        elif isDelivery(request):
            deliveryOrders = Order.objects.filter(delivery_crew=request.user)
            serializer = self.get_serializer(deliveryOrders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Customers
        elif isCustomer(request):
            userOreders = Order.objects.filter(user=request.user)
            serializer = self.get_serializer(userOreders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"You are not allowed here!!"}, status=status.HTTP_403_FORBIDDEN)

    # Create new order (Must be a customer and has items in his cart) then create OrderItem for every menuItem in your Cart and finally delete the cart.
    def create(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        # Customer has no groups and has items in his cart
        if isCustomer(request) and len(cart) != 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create the oreder
            order = Order.objects.create(
                    user = request.user,
                    total = 0,
                    date = serializer.data.get('date')
                )
            order.save()
            total = 0
            # Create OrderItem for every menuItem in your Cart.
            for cartObject in cart:
                orderItem = OrderItem.objects.create(
                    order = order,
                    menuItem = cartObject.menuItem,
                    quantity = cartObject.quantity,
                    unit_price = cartObject.unit_price,
                    price = cartObject.price
                )
                # Get the total price
                total += cartObject.price
                orderItem.save()
            # Add the total price to the order object
            order.total = total
            order.save()
            # Delete the cart
            cart.delete()
            return Response({"Your order has been completed."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Your cart does't have any items!"}, status = status.HTTP_403_FORBIDDEN)

    # Delete order with pk
    def destroy(self, request, *args, **kwargs):
        if isManager(request) or request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"You don't have permissions"}, status = status.HTTP_403_FORBIDDEN)

    # Get order with pk
    def retrieve(self, request, *args, **kwargs):
        orderItems = OrderItem.objects.filter(order__pk=dict(**kwargs)['pk'])
        order = Order.objects.get(pk=dict(**kwargs)['pk'])
        if len(orderItems) != 0:
            if (request.user == order.user or request.user.is_superuser):
                serializer = OrderItemSerializer(orderItems, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"You don't have permissions or it is not your order"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Updates the order. A manager can use this endpoint to set a delivery crew to this order
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if isManager(request):
            serializer = ManagerOrderSerializer(order, data=request.data)
        elif isCustomer(request) and order.user == request.user:
            serializer = OrderSerializer(order, data=request.data, partial=True)
        else:
            return Response({"You don't have permissions"}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial Update the order. A manager can use this endpoint to set a delivery crew to this order, A delivery crew can use this endpoint to update the order status to 0 or 1.
    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        if isDelivery(request) and order.delivery_crew == request.user:
            serializer = DeliveryOrderSerializer(order, data=request.data, partial=True)
        elif isManager(request):
            serializer = ManagerOrderSerializer(order, data=request.data, partial=True)
        elif isCustomer(request) and order.user == request.user:
            serializer = OrderSerializer(order, data=request.data, partial=True)
        else:
            return Response({"You don't have permissions"}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)