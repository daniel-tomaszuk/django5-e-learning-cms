from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """
    Custom OrderField that will automatically set order position (`self.attname`)
    taking previous model instances into account.
    """

    def __init__(self, for_fields: list[str] | None = None, *args, **kwargs):
        self.for_fields: list[str] = for_fields  # fields used to order the data
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: models.Model, add):
        """
        Return field's value just before saving.
        Increment order value.
        """

        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                queryset = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in `for_fields`
                    query_kwargs = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    queryset = queryset.filter(**query_kwargs)
                # get the order of the last item
                last_item = queryset.latest(self.attname)
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value

        # if there already is order value, do not recalculate, just return the value
        return super().pre_save(model_instance, add)
