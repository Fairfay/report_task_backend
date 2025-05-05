from django.urls import include, path


# Настройка URL-маршрутов для аутентификации через Djoser с поддержкой JWT
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
