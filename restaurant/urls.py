from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    TableViewSet, 
    SectionViewSet, 
    RestaurantViewSet,
    TableDetailView,
    MenuChoiceView,
    PredCheckView,
    CallWaiterView
)

router = DefaultRouter()
router.register(r'tables', TableViewSet, basename='table')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('api/', include(router.urls)),
    path('<uuid:uuid>/', TableDetailView.as_view(), name='table_detail'),
    path('<uuid:uuid>/menu/', MenuChoiceView.as_view(), name='menu_choice'),
    path('<uuid:uuid>/check/', PredCheckView.as_view(), name='pred_check'),
    path('<uuid:uuid>/call-waiter/', CallWaiterView.as_view(), name='call_waiter'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)