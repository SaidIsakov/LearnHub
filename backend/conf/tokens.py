from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema_view(
    post=extend_schema(tags=['auth'])
)
class TaggedTokenObtainPairView(TokenObtainPairView):
    pass



@extend_schema_view(
    post=extend_schema(tags=['auth'])
)
class TaggedTokenRefreshView(TokenRefreshView):
    pass
