from django.urls import include
from django.urls import path
from rest_framework import routers

from courses.api import views

app_name = "courses"


router = routers.DefaultRouter()
router.register("courses", views.CourseViewSet)
router.register("subjects", views.SubjectViewSet)


urlpatterns = [
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("", include(router.urls)),
]
