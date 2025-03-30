from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, Wishlist, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) 

    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer() 

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  

    class Meta:
        model = Cart
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  

    class Meta:
        model = Wishlist
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
