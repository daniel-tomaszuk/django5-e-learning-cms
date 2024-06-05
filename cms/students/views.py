from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView
from students.forms import CourseEnrollForm

User = get_user_model()


class StudentRegistrationView(CreateView):
    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("student_course_list")

    def form_valid(self, form) -> HttpResponse:
        is_valid: HttpResponse = super().form_valid(form)
        cleaned_data: dict = form.cleaned_data
        user: User = authenticate(
            cleaned_data.get("username"), password=cleaned_data.get("password")
        )
        login(self.request, user)
        return is_valid


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form) -> HttpResponse:
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("student_course_detail", args=[self.course.id])
