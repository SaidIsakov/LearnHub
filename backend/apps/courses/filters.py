import django_filters
from .models import Course, Lesson


import django_filters
from .models import Course


class CourseFilter(django_filters.FilterSet):
  title = django_filters.CharFilter(lookup_expr='icontains')
  is_published = django_filters.BooleanFilter()

  class Meta:
    model = Course
    fields = ['title','is_published']



class LessonFilter(django_filters.FilterSet):
  title = django_filters.CharFilter(lookup_expr='icontains')
  is_published = django_filters.BooleanFilter()

  class Meta:
    model = Lesson
    fields = ['title','is_published']
