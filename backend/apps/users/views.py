from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import authentication
from apps.users.ai_recommendation import ai_give_recommendations
from .services import get_recommendation_context
from django.contrib.auth import get_user_model
from apps.users.models import AIRecommendation
from rest_framework.permissions import IsAuthenticated


class ListRecommendation(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user

    context = get_recommendation_context(user)
    ai_recommendations = ai_give_recommendations(context)
    AIRecommendation.objects.update_or_create(
        user = user,
        defaults = {
          "summary": ai_recommendations['summary'],
          "strengths": ai_recommendations['strengths'],
          "weaknesses": ai_recommendations['weaknesses'],
          "next_goal":  ai_recommendations['next_goal'],
          "motivation":  ai_recommendations['motivation']
        }
      )
    return Response({"recommendations": ai_recommendations})
