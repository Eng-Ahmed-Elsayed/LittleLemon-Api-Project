# Little Lemon Api Project using Django, Django-rest-framework, djoser

## Scope:-

A fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders.

## Features

* ### Authentiaction

  * Token Based Authentication

  * Jwt Based Authentication

  * Session Authentication

* ### Filtering, searching and Pagination

* ### Throttling

* ### Custom function and class-based views

* ### Custom function and class-based serializers

* ### Custom permissions and authorization

## Available API endpoints using django-rest-framework

* ### User registration and token generation endpoints

| Endpoint  | Role | Method | Purpose |
| ------------- | ------------- | ------------- | ------------- |
| admin/  | admin only  |  - | Django administration   |
| /api/users/users/me/  | Anyone with a valid user token  | GET | Displays only the current user  |
| /token/login/  | Anyone with a valid username and password  | POST | Generates access tokens that can be used in other API calls in this project  |

* ### Menu-items endpoints

| Endpoint  | Role | Method | Purpose |
| ------------- | ------------- | ------------- | ------------- |
| /api/menu-items  | Customer, delivery crew  | GET  | Lists all menu items. Return a 200 – Ok HTTP status code  |
| /api/menu-items  | Customer, delivery crew  | POST, PUT, PATCH, DELETE  | Denies access and returns 403 – Unauthorized HTTP status code  |
| /api/menu-items/{menuItem}  | Customer, delivery crew  | GET  | Lists single menu item  |
| /api/menu-items/{menuItem}  | Customer, delivery crew  | POST, PUT, PATCH, DELETE  | Returns 403 - Unauthorized  |
| /api/menu-items  | Manager  | GET   | Lists all menu items  |
| /api/menu-items  | Manager  | POST, PATCH  | Updates single menu item  |
| /api/menu-items  | Manager  | DELETE | Deletes menu item  |

* ### User group management endpoints

| Endpoint  | Role | Method | Purpose |
| ------------- | ------------- | ------------- | ------------- |
| /api/groups/manager/users  | Manager  | GET  | Returns all managers  |
| /api/groups/manager/users  | Manager  | POST  | Assigns the user in the payload to the manager group and returns 201-Created  |
| /api/groups/manager/users/{userId}  | Manager  | DELETE  | Removes this particular user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found  |
| /api/groups/delivery-crew/users  | Manager  | GET  | Returns all delivery crew  |
| /api/groups/delivery-crew/users  | Manager  | POST  | Assigns the user in the payload to delivery crew group and returns 201-Created HTTP  |
| /api/groups/delivery-crew/users/{userId}  | Manager  | DELETE | Removes this user from the manager group and returns 200 – Success if everything is okay.

If the user is not found, returns  404 – Not found  |

* ### Cart management endpoints

| Endpoint  | Role | Method | Purpose |
| ------------- | ------------- | ------------- | ------------- |
| /api/cart/menu-items  | Customer  | GET  | Returns current items in the cart for the current user token  |
| /api/cart/menu-items  | Customer  | POST  | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items  |
| /api/cart/menu-items  | Customer  | DELETE  | Deletes all menu items created by the current user token  |

* ### Order management endpoints

| Endpoint  | Role | Method | Purpose |
| ------------- | ------------- | ------------- | ------------- |
| /api/orders  | Customer  | GET  | Returns all orders with order items created by this user |
| /api/orders  | Customer  | POST  | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user. |
| /api/orders/{orderId}  | Customer  | GET  | Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.  |
| /api/orders  | Manager  | GET  | Returns all orders with order items by all users  |
| /api/orders/{orderId}  | Manager  | PUT, PATCH  | Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1. If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery. If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered. |
| /api/orders/{orderId}  | Manager  | DELETE  | Deletes this order |
| /api/orders  | Delivery crew  | GET  | Returns all orders with order items assigned to the delivery crew  |
| /api/orders  | Delivery crew  | PATCH  | A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.  |

## Available auth endpoints using djoser

| Endpoint |
| ------------- |
| auth/users/ |
| auth/users/me/ |
| auth/users/confirm/ |
| auth/users/resend_activation/ |
| auth/users/set_password/ |
| auth/users/reset_password/ |
| auth/users/reset_password_confirm/ |
| auth/users/set_username/ |
| auth/users/reset_username/ |
| auth/users/reset_username_confirm/ |
| auth/token/login/ (Token Based Authentication) |
| auth/token/logout/ (Token Based Authentication) |
| auth/jwt/create/ (JSON Web Token Authentication) |
| auth/jwt/refresh/ (JSON Web Token Authentication) |
| auth/jwt/verify/ (JSON Web Token Authentication) |

## Users

The username is also the passsword for all users
| Username/passsword | Role |
| ------------- | ------------- |
| test123 | Superuser |  
| nfaire9 | Manager |
| acozby0 | Manager |
| ahullah1 | Delivery Crew |
| gmorican2 | Delivery Crew |
| msarjant6 | Customer(No groups) |
| rotter7 | Customer(No groups) |

## Screenshots

![Auth login to generate token](./images/1-auth login to generate token.png)

![Add menu-item with token 1](./images/2-Add menu-item with token 1.png)

![Add menu-item with token 2](./images/3-Add menu-item with token 2.png)

![List all menu-items with token](./images/4-List all menu-items with token.png)

![Get menu-item with token](./images/5-get menu-item with token.png)

![Post item to the cart customer](./images/6-Post item to the cart customer.png)

![Other api points](./images/other api points)
