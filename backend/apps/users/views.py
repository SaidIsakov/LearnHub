from rest_framework.response import Response
from rest_framework.views import APIView
from .services import RecommendationService
from rest_framework.permissions import IsAuthenticated



class RecommendationAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user

    ai_recommendations = RecommendationService.generate(user)

    return Response({"recommendations": ai_recommendations})
