from django.contrib import admin

from courses.models import Course
from courses.models import Module
from courses.models import Product
from courses.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [Subject.Keys.title, Subject.Keys.slug]
    prepopulated_fields = {Subject.Keys.slug: (Subject.Keys.title,)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "quantity", "price"]


class ModuleInLine(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [Course.Keys.title, Course.Keys.subject, Course.Keys.created]
    list_filter = [Course.Keys.created, Course.Keys.subject]
    search_fields = [Course.Keys.title, Course.Keys.overview]
    prepopulated_fields = {Course.Keys.slug: (Course.Keys.title,)}
    inlines = [ModuleInLine]
