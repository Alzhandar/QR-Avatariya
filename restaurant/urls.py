from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'tables', views.TableViewSet, basename='table')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('api/', include(router.urls)),
    path('<uuid:uuid>/',views.TableDetailView.as_view(), name='table_detail')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)