from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, ProductViewSet, 
    AddToCartView, ViewCartView, AddToWishlistView, ViewWishlistView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('view-cart/', ViewCartView.as_view(), name='view_cart'),
    path('add-to-wishlist/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('view-wishlist/', ViewWishlistView.as_view(), name='view_wishlist'),
    path('', include(router.urls)),
]