from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns = [

    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),


    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),


    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]
