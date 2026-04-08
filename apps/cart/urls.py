from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r'', CartItemViewSet, basename='cart')

urlpatterns = router.urls
