from django.urls import path
from . import views

urlpatterns = [
    path('buyer/', views.buyer_dashboard),
    path('seller/', views.seller_dashboard),

    path('negotiations/', views.my_negotiations),
    path('negotiations/<int:negotiation_id>/', views.negotiation_detail),
    path('negotiations/<int:negotiation_id>/status/', views.update_negotiation_status),

    path('favorites/', views.my_favorites),
    path('favorites/add/', views.add_favorite),
    path('favorites/<int:favorite_id>/delete/', views.remove_favorite),

    path('notifications/', views.my_notifications),
    path('notifications/create/', views.create_notification),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read),
    path('buyer-page/', views.buyer_dashboard_page),
    path('seller-page/', views.seller_dashboard_page),
    path('negotiations-page/', views.negotiations_page),
    path('favorites-page/', views.favorites_page),
    path('notifications-page/', views.notifications_page),
    path('sell-item-page/', views.sell_item_page),
]