from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer
from courses.api.serializers import SubjectSerializer
from courses.models import Course
from courses.models import Subject


class SubjectListView(ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count(Subject.Keys.courses))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class SubjectDetailView(RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count(Subject.Keys.courses))
    serializer_class = SubjectSerializer


class CourseListView(ListAPIView):
    queryset = Course.objects.prefetch_related(Course.Keys.modules).all()
    serializer_class = CourseSerializer
