from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from inventory import views as inventory_views

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory API",
        default_version='v1',
        description="API documentation for the Inventory System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@inventory.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/', inventory_views.add_item),
    path('remove/', inventory_views.remove_item),
    path('stock_level/<str:item_name>', inventory_views.get_stock_level),
    path('all_stock_levels/', inventory_views.get_all_stock_levels),
    path('critical_notifications/', inventory_views.get_critical_notifications),
    path('history/export/', inventory_views.export_history),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
