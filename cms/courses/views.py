from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from courses.models import Course


class OwnerMixin:
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form) -> bool:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = [
        Course.Keys.subject,
        Course.Keys.title,
        Course.Keys.slug,
        Course.Keys.overview,
    ]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "courses/manage/course/list.html"

    def get_queryset(self) -> QuerySet[Course]:
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
