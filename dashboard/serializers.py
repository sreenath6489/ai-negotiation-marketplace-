from rest_framework import serializers
from .models import Favorite, Notification
from negotiations.models import Negotiation


class FavoriteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'created_at']


class NegotiationSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Negotiation
        fields = [
            'id', 'buyer', 'seller', 'product',
            'product_name', 'buyer_name', 'seller_name',
            'current_offer', 'status', 'created_at', 'updated_at'
        ]