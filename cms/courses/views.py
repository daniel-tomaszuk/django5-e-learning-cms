from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.db.models import QuerySet
from django.forms import Form
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import View

from courses.forms import ModuleFormSet
from courses.models import Content
from courses.models import Course
from courses.models import File
from courses.models import Image
from courses.models import Module
from courses.models import Text
from courses.models import Video


class OwnerMixin:
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form) -> bool:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
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
    permission_required = ["courses.view_course"]

    def get_queryset(self) -> QuerySet[Course]:
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = ["courses.add_course"]


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = ["courses.change_course"]


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = ["courses.delete_course"]


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/formset.html"
    course = None

    def dispatch(self, request, *args, **kwargs):
        pk: str = kwargs.get("pk")

        # is fine, each request creates a new instance of the view with `course = None` at the beginning
        self.course = get_object_or_404(
            Course,
            id=pk,
            owner=self.request.user,
        )
        return super().dispatch(request=request, pk=pk)

    def get_formset(self, data: dict | None = None):
        return ModuleFormSet(instance=self.course, data=data)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(dict(course=self.course, formset=formset))

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_course_list")
        return self.render_to_response(dict(course=self.course, formset=formset))


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    Handles creation / update of different module contents.
    """

    SUPPORTED_CONTENT_TYPES = {
        "text": Text,
        "video": Video,
        "image": Image,
        "file": File,
    }

    # Used between methods - each request makes new instance of the view so it's fine (None is non mutable)
    module = None
    model = None
    obj = None

    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name: str) -> models.Model | None:
        return self.SUPPORTED_CONTENT_TYPES.get(model_name)

    def get_form(self, model, *args, **kwargs) -> Form:
        form = modelform_factory(
            model, exclude=["owner", "order", "created", "updated"]
        )
        return form(*args, **kwargs)

    def dispatch(
        self, request, module_id: int, model_name: str, *args, id: int = None, **kwargs
    ) -> TemplateResponse:
        self.module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user,
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super().dispatch(
            *args,
            request=request,
            module_id=module_id,
            model_name=model_name,
            id=id,
            **kwargs,
        )

    def get(self, request, module_id: int, model_name: str, id: int | None = None):
        form = self.get_form(
            model=self.model,
            instance=self.obj,
        )
        return self.render_to_response(context=dict(form=form, object=self.obj))

    def post(self, request, module_id: int, model_name: str, id: int | None = None):
        form = self.get_form(
            model=self.model, instance=self.obj, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:  # new content is created
                Content.objects.create(module=self.module, item=obj)
            return redirect("module_content_list", self.module.id)
        return self.render_to_response(context=dict(form=form, object=self.obj))


class ContentDeleteView(View):

    def post(self, request, id: int):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect("module_content_list", module.id)
