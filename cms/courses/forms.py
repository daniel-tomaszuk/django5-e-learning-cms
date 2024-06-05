from django.forms import inlineformset_factory

from courses.models import Course
from courses.models import Module

ModuleFormSet = inlineformset_factory(
    parent_model=Course,
    model=Module,
    fields=[Module.Keys.title, Module.Keys.description],
    extra=2,
    can_delete=True,
)
