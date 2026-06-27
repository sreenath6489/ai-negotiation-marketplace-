from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm, ReviewForm
from .models import Order, Review

# API Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer, ReviewSerializer


# Checkout
def checkout(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            # Calculate total amount (₹100 per item)
            order.total_amount = order.quantity * 100

            order.save()

            return redirect("payment")

    else:
        form = OrderForm()

    return render(request, "checkout.html", {"form": form})


# Payment
def payment(request):
    orders = Order.objects.order_by("-id")

    if request.method == "POST":
        order_id = request.POST.get("order_id")

        order = get_object_or_404(Order, id=order_id)
        order.status = "Confirmed"
        order.save()

        return redirect("order_success")

    return render(request, "payment.html", {"orders": orders})


# Order Success
def order_success(request):
    return render(request, "order_success.html")


# Purchase History
def purchase_history(request):
    orders = Order.objects.all()
    return render(request, "purchase_history.html", {"orders": orders})


# Sales History
def sales_history(request):
    orders = Order.objects.all().order_by("-order_date")
    return render(request, "sales_history.html", {"orders": orders})


# Add Review
def add_review(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.save()

            return redirect("purchase_history")

    else:
        form = ReviewForm()

    return render(request, "review.html", {
        "form": form,
        "order": order,
    })


# Invoice
def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, "invoice.html", {
        "order": order
    })


# Test Page
def test_view(request):
    return render(request, "test.html")


@api_view(["GET"])
def order_api(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def review_api(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)