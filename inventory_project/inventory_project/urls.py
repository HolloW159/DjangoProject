from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from inventory import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/', inventory_views.add_item, name='add_item'),
    path('remove/', inventory_views.remove_item, name='remove_item'),
    path('stock_level/<str:item_name>/', inventory_views.get_stock_level, name='get_stock_level'),
    path('all_stock_levels/', inventory_views.get_all_stock_levels, name='get_all_stock_levels'),
    path('critical_notifications/', inventory_views.get_critical_notifications, name='get_critical_notifications'),
    path('history/export/', inventory_views.export_history, name='export_history'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
