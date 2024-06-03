from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subject(models.Model):

    class Keys:
        id = "id"
        title = "title"
        slug = "slug"

        # relations
        courses = "courses"

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return str(self.title)


class Course(models.Model):

    class Keys:
        id = "id"
        title = "title"
        slug = "slug"
        overview = "overview"
        created = "created"
        updated = "updated"

        # relations
        owner = "owner"
        subject = "subject"
        modules = "modules"

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return str(self.title)


class Module(models.Model):

    class Keys:
        id = "id"
        title = "title"
        description = "description"
        course = "course"

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.title)
