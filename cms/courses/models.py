from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from courses.fields import OrderField

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
        students = "students"

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
    students = models.ManyToManyField(
        User, related_name="courses_joined", blank=True, null=True
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
        order = "order"

        # relations
        course = "course"
        contents = "contents"

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.order}. {self.title}"


class Content(models.Model):
    class Keys:
        id = "id"
        order = "order"

        module = "module"
        content_type = "content_type"
        object_id = "object_id"
        item = "item"

    order = OrderField(blank=True, for_fields=["module"])
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )

    # generic key used to point at different models, only few are allowed
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": ("text", "video", "image", "file"),
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["order"]


class ItemBase(models.Model):
    class Keys:
        id = "id"
        title = "title"
        created = "created"
        updated = "updated"

        owner = "owner"

    title = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.title)

    def render(self):
        """
        Returns given item dedicated HTML that should be displayed
        """
        return render_to_string(
            f"courses/content/{self._meta.model_name}.html", context=dict(item=self)
        )


class Text(ItemBase):
    class Keys:
        id = "id"
        title = "title"
        created = "created"
        updated = "updated"
        owner = "owner"

        content = "content"

    content = models.TextField()


class File(ItemBase):
    UPLOAD_DIR = "files"

    class Keys:
        id = "id"
        title = "title"
        created = "created"
        updated = "updated"
        owner = "owner"

        file = "file"

    file = models.FileField(upload_to=UPLOAD_DIR)


class Image(ItemBase):
    UPLOAD_DIR = "images"

    class Keys:
        id = "id"
        title = "title"
        created = "created"
        updated = "updated"
        owner = "owner"

        file = "file"

    file = models.FileField(upload_to=UPLOAD_DIR)


class Video(ItemBase):

    class Keys:
        id = "id"
        title = "title"
        created = "created"
        updated = "updated"
        owner = "owner"

        url = "url"

    url = models.URLField()
