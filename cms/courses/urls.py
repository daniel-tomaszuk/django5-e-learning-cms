from django.urls import path

from courses import views

urlpatterns = [
    path("mine/", views.ManageCourseListView.as_view(), name="manage_course_list"),
    path("create/", views.CourseCreateView.as_view(), name="course_create"),
    path("<int:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
]
