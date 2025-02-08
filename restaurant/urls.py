from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

router = DefaultRouter()
router.register(r'tables', views.TableViewSet, basename='table')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('api/', include(router.urls)),
    path('<uuid:uuid>/', TableDetailView.as_view(), name='table_detail'),
    path('<uuid:uuid>/menu/', MenuChoiceView.as_view(), name='menu_choice'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)