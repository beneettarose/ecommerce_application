from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Product, Category, Cart, CartItem, Wishlist
from .serializers import (
    ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer,
    WishlistSerializer, UserSerializer, RegisterSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authtoken.models import Token



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__name']
    ordering_fields = ['price']

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if category:
            queryset = queryset.filter(category__name=category)
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        cart, created = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({"message": "Product added to cart!"}, status=status.HTTP_201_CREATED)


class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({"message": "Cart is empty"}, status=status.HTTP_200_OK)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        wishlist, created = Wishlist.objects.get_or_create(user=user)
        product = Product.objects.get(id=product_id)
        wishlist.products.add(product)

        return Response({"message": "Product added to wishlist!"}, status=status.HTTP_201_CREATED)


class ViewWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wishlist = Wishlist.objects.filter(user=user).first()
        if not wishlist:
            return Response({"message": "Wishlist is empty"}, status=status.HTTP_200_OK)
        
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


