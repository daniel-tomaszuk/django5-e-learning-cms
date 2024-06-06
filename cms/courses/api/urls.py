from django.urls import path

from courses.api import views

app_name = "courses"
urlpatterns = [
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path(
        "subjects/<int:pk>/", views.SubjectDetailView.as_view(), name="subject_detail"
    ),
    path("courses/", views.CourseListView.as_view(), name="course_list"),
]
