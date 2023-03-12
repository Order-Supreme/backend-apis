from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static



router = SimpleRouter()
router.register("fastrack/restaurant", views.RestaurantViewSet)
router.register("fastrack/customer", views.CustomerViewSet)
router.register("fastrack/table", views.TableViewSet)
router.register("fastrack/payment", views.PaymentViewSet)
router.register("fastrack/image", views.ImageViewSet)
router.register("fastrack/menu", views.MenuViewSet)
router.register("fastrack/booked_table", views.BookedTableViewSet)
router.register("fastrack/order", views.OrderViewSet, basename='order')
router.register("fastrack/inventory", views.InventoryViewSet)

urlpatterns = router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path('fastrack/home/', views.home),
#     path('fastrack/restaurant/', views.restaurant_all)
# ]
