from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoriesModelView.as_view(
        {
            'get': 'list',
        	'post': 'create',
        }
    )),
    path('menu-items', views.MenuItemModelView.as_view(
        {
        	'get': 'list',
        	'post': 'create',
    	})
    ),
    path('menu-items/<int:pk>', views.MenuItemModelView.as_view(
        {
        	'get': 'retrieve',
        	'put': 'update',
        	'patch': 'partial_update',
        	'delete': 'destroy',
    	})
    ),
    path('cart/menu-items', views.CartModelView.as_view(
        {
        	'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            
        }
    )),
    path('orders', views.OrdersModelView.as_view(
        {
        	'get': 'list',
            'post': 'create',
            
        }
    )),
    path('orders/<int:pk>', views.OrdersModelView.as_view(
        {
        	'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update',

        }
    )),
    path('groups/manager/users', views.ManagersListView),
    path('groups/manager/users/<int:pk>', views.ManagersCreateDeleteView),
    path('groups/delivery-crew/users', views.DeliveryCrewListView),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewCreateDeleteView),
]