from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from apps.courses.urls import router as course_router
from apps.assignments.urls import router as assignment_router
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .tokens import TaggedTokenObtainPairView, TaggedTokenRefreshView
from apps.users.views import RecommendationAPIView


router = routers.DefaultRouter()

router.registry.extend(course_router.registry)
router.registry.extend(assignment_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    #drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    #JWT
    path('api/auth/token/', TaggedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TaggedTokenRefreshView.as_view(), name='token_refresh'),

    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # User
    path('users/recommendations/', RecommendationAPIView.as_view(), name='recommendations')
]
