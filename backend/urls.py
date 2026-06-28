from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from orders import views as orders_views
from dashboard import views as dashboard_views

urlpatterns = [
    # Marketplace
    path('', include('marketplace.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # Token APIs
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # Dashboard
    path('api/dashboard/', include('dashboard.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('sell-item/', dashboard_views.sell_item_page, name='sell_item_page'),

    # Orders
    path('checkout/', orders_views.checkout, name='checkout'),
    path('payment/', orders_views.payment, name='payment'),
    path('success/', orders_views.order_success, name='order_success'),
    path('purchase-history/', orders_views.purchase_history, name='purchase_history'),
    path('sales-history/', orders_views.sales_history, name='sales_history'),
    path('review/<int:order_id>/', orders_views.add_review, name='add_review'),
    path('invoice/<int:order_id>/', orders_views.invoice, name='invoice'),
    path('test/', orders_views.test_view, name='test'),

    # REST APIs
    path('api/orders/', orders_views.order_api, name='order_api'),
    path('api/reviews/', orders_views.review_api, name='review_api'),
]