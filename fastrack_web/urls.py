from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("fastrack/restaurant", views.RestaurantViewSet)
router.register("fastrack/table", views.TableViewSet)
router.register("fastrack/payment", views.PaymentViewSet)
router.register("fastrack/image", views.ImageViewSet)
router.register("fastrack/menu", views.MenuViewSet)
router.register("fastrack/booked_table", views.BookedTableViewSet)
router.register("fastrack/order", views.OrderViewSet)
router.register("fastrack/inventory", views.InventoryViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('fastrack/home/', views.home),
#     path('fastrack/restaurant/', views.restaurant_all)
# ]
