from django.db.models import Count
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from courses.api.pagination import StandardPagination
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseSerializer
from courses.api.serializers import CourseWithContentSerializer
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


class SubjectViewSet(ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count(Subject.Keys.courses))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class CourseListView(ListAPIView):
    queryset = Course.objects.prefetch_related(Course.Keys.modules).all()
    serializer_class = CourseSerializer


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related(Course.Keys.modules)
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs) -> Response:
        course: Course = self.get_object()
        course.students.add(request.user)
        return Response()

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseWithContentSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int, format=None) -> Response:
        course: Course = get_object_or_404(Course, id=pk)
        course.students.add(request.user)
        return Response()
