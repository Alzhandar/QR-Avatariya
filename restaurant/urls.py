from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tables', views.TableViewSet, basename='table')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('api/', include(router.urls)),
]