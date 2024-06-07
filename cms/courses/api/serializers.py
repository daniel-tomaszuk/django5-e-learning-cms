from django.db.models import Count
from rest_framework import serializers

from courses.models import Content
from courses.models import Course
from courses.models import ItemBase
from courses.models import Module
from courses.models import Subject


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value: ItemBase) -> str:
        return value.render()


class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            Subject.Keys.id,
            Subject.Keys.title,
            Subject.Keys.slug,
            "total_courses",
            "popular_courses",
        ]

    def get_popular_courses(self, obj: Subject) -> list[str]:
        courses = obj.courses.annotate(
            total_students=Count(Course.Keys.students)
        ).order_by("total_students")[:3]
        return [f"{course.title} ({course.total_students})" for course in courses]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    modules = ModuleSerializer(many=True, read_only=True)


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = [Content.Keys.order, Content.Keys.item]


class ModuleWithContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = [
            Module.Keys.order,
            Module.Keys.title,
            Module.Keys.description,
            Module.Keys.contents,
        ]


class CourseWithContentSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"
