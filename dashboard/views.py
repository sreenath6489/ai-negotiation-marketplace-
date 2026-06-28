from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


from marketplace.models import Product
from negotiations.models import Negotiation
from .models import Favorite, Notification
from .serializers import FavoriteSerializer, NotificationSerializer, NegotiationSerializer
from django.shortcuts import render

def profile_setup(request):
    if request.method == "POST":
        request.user.phone = request.POST.get("phone")
        request.user.location = request.POST.get("location")
        request.user.save()

        return redirect("/api/dashboard/sell-item-page/")

    return render(request, "dashboard/profile_setup.html")

@api_view(['GET'])
def buyer_dashboard(request):
    user = request.user
    data = {
        "total_negotiations": Negotiation.objects.filter(buyer=user).count(),
        "active_negotiations": Negotiation.objects.filter(buyer=user, status="active").count(),
        "accepted_deals": Negotiation.objects.filter(buyer=user, status="accepted").count(),
        "favorite_products": Favorite.objects.filter(user=user).count(),
        "unread_notifications": Notification.objects.filter(user=user, is_read=False).count(),
    }
    return Response(data)


@api_view(['GET'])
def seller_dashboard(request):
    user = request.user
    data = {
        "total_negotiations": Negotiation.objects.filter(seller=user).count(),
        "active_negotiations": Negotiation.objects.filter(seller=user, status="active").count(),
        "accepted_deals": Negotiation.objects.filter(seller=user, status="accepted").count(),
        "unread_notifications": Notification.objects.filter(user=user, is_read=False).count(),
    }
    return Response(data)


@api_view(['GET'])
def my_negotiations(request):
    negotiations = Negotiation.objects.filter(buyer=request.user) | Negotiation.objects.filter(seller=request.user)
    serializer = NegotiationSerializer(negotiations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def my_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def negotiation_detail(request, negotiation_id):
    negotiation = get_object_or_404(Negotiation, id=negotiation_id)
    serializer = NegotiationSerializer(negotiation)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_negotiation_status(request, negotiation_id):
    negotiation = get_object_or_404(Negotiation, id=negotiation_id)

    status = request.data.get("status")

    if status not in ["pending", "active", "accepted", "rejected", "cancelled"]:
        return Response({"error": "Invalid status"}, status=400)

    negotiation.status = status
    negotiation.save()

    return Response({
        "message": "Negotiation status updated successfully",
        "status": negotiation.status
    })


@api_view(['POST'])
def add_favorite(request):
    product_id = request.data.get('product')

    if not product_id:
        return Response({"error": "Product ID is required"}, status=400)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product_id=product_id
    )

    if created:
        return Response({"message": "Product added to favorites"}, status=201)

    return Response({"message": "Product is already in favorites"}, status=200)


@api_view(['DELETE'])
def remove_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return Response({"message": "Favorite removed successfully"})


@api_view(['POST'])
def create_notification(request):
    title = request.data.get('title')
    message = request.data.get('message')

    if not title or not message:
        return Response({"error": "Title and message are required"}, status=400)

    notification = Notification.objects.create(
        user=request.user,
        title=title,
        message=message
    )

    serializer = NotificationSerializer(notification)
    return Response(serializer.data, status=201)


@api_view(['PATCH'])
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return Response({"message": "Notification marked as read"})


def buyer_dashboard_page(request):
    recent_negotiations = Negotiation.objects.filter(buyer=request.user).order_by('-created_at')[:5]

    context = {
        "total_negotiations": Negotiation.objects.filter(buyer=request.user).count(),
        "active_negotiations": Negotiation.objects.filter(buyer=request.user, status="active").count(),
        "accepted_deals": Negotiation.objects.filter(buyer=request.user, status="accepted").count(),
        "favorite_products": Favorite.objects.filter(user=request.user).count(),
        "unread_notifications": Notification.objects.filter(user=request.user, is_read=False).count(),
        "recent_negotiations": recent_negotiations,
    }

    return render(request, "dashboard/buyer_dashboard.html", context)


def seller_dashboard_page(request):
    recent_negotiations = Negotiation.objects.filter(seller=request.user).order_by('-created_at')[:5]
    my_products = Product.objects.filter(seller=request.user).order_by('-created_at')

    context = {
        "total_negotiations": Negotiation.objects.filter(seller=request.user).count(),
        "active_negotiations": Negotiation.objects.filter(seller=request.user, status="active").count(),
        "accepted_deals": Negotiation.objects.filter(seller=request.user, status="accepted").count(),
        "unread_notifications": Notification.objects.filter(user=request.user, is_read=False).count(),
        "recent_negotiations": recent_negotiations,
        "my_products": my_products,
    }

    return render(request, "dashboard/seller_dashboard.html", context)


def negotiations_page(request):
    negotiations = Negotiation.objects.filter(buyer=request.user) | Negotiation.objects.filter(seller=request.user)
    return render(request, "dashboard/negotiations.html", {"negotiations": negotiations})


def favorites_page(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, "dashboard/favorites.html", {"favorites": favorites})


def notifications_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "dashboard/notifications.html", {"notifications": notifications})


def sell_item_page(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/")

    if not request.user.phone or not request.user.location:
        return redirect("/api/dashboard/profile-setup/")

    if request.method == "POST":
        Product.objects.create(
            seller=request.user,
            title=request.POST.get("name"),
            category=request.POST.get("category"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
            image=request.FILES.get("image")
        )

        return redirect("/")

    return render(request, "dashboard/sell_item.html")