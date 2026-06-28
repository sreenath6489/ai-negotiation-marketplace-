from django.contrib import admin
from django.urls import path, include
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dashboard/', include('dashboard.urls')),

    # Checkout
    path('', include('marketplace.urls')),
    path('payment/', views.payment, name='payment'),
    path('success/', views.order_success, name='order_success'),

    # Order History
    path('purchase-history/', views.purchase_history, name='purchase_history'),
    path('sales-history/', views.sales_history, name='sales_history'),

    # Review
    path('review/<int:order_id>/', views.add_review, name='add_review'),

    # Invoice
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),

    # Test
    path('test/', views.test_view, name='test'),

    # REST APIs
    path('api/orders/', views.order_api, name='order_api'),
    path('api/reviews/', views.review_api, name='review_api'),
    path('api/accounts/', include('accounts.urls')),
]