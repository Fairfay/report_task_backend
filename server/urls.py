from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from referential.views import (
    DeliveryViewSet, TransportViewSet,
    FileViewSet, FileUploadAPIView,
    ServiceViewSet, StatisticsViewSet
)


router = DefaultRouter()
router.register(r'transports', TransportViewSet, basename='transports')
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'deliverys', DeliveryViewSet, basename='deliverys')
router.register(r'files', FileViewSet, basename='files')
router.register(r'statistics', StatisticsViewSet, basename='statistics')

urlpatterns = [
    path('api/identity/', include('identity.urls')),
    path('api/v1/', include(router.urls)),
    path('api/admin/', admin.site.urls),
    path('api/upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
