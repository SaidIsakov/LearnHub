from django.shortcuts import render
from apps.assignments.models import Assignment, Submission
from apps.assignments.serializers import AssignmentSerializer, SubmissionSerializer
from apps.assignments.permissions import CanCreateAssignment, CanReviewSubmission, \
                                         CanSubmitWork
from apps.courses.models import CourseMember, CourseRole
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet



class AssignmentViewSet(ModelViewSet):
  serializer_class = AssignmentSerializer

  def perform_create(self, serializer):
    lesson_id = self.request.data.get('lesson')
    serializer.save(
        created_by = self.request.user,
        lesson_id = lesson_id
    )

  def get_queryset(self):
    user = self.request.user
    return Assignment.objects.filter(
        lesson__course__members__user=user
    ).distinct()

  def get_permissions(self):
    if self.action == 'create':
      return [CanCreateAssignment()]
    return [IsAuthenticated()]



class SubmissionViewSet(ModelViewSet):
  serializer_class = SubmissionSerializer

  def perform_create(self, serializer):
    assignment_id = self.request.data.get('assignment')
    serializer.save(
        student = self.request.user,
        assignment_id = assignment_id
    )

  def get_queryset(self):
    user = self.request.user

    full_access = CourseMember.objects.filter(
        user=user,
        role__in = [CourseRole.INSTRUCTOR, CourseRole.TEACHING_ASSISTANT],
        is_active = True
    ).values_list('course_id', flat=True)

    submissions = Submission.objects.none()

    if full_access:
      submissions |= Submission.objects.filter(
          assignment__lesson__course_id__in=full_access
      )
    submissions |= Submission.objects.filter(student=user)

    return submissions.distinct()

  def get_permissions(self):
    if self.action == 'create':
      return [CanSubmitWork()]
    if self.action in ['update', 'partial_update']:
      return [CanReviewSubmission()]
    return [IsAuthenticated()]
