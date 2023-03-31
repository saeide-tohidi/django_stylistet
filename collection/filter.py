import django_filters
from django_filters import filters

from attribute.models import AssignedProductAttribute, AssignedProductAttributeValue
from product.models import Product, ProductType


class CustomField(django_filters.fields.ModelMultipleChoiceField):
    def _check_values(self, value):
        """
        Override the base class' _check_values method so our queryset is not
        empty if one of the items in value is invalid.
        """
        null = self.null_label is not None and value and self.null_value in value
        if null:
            value = [v for v in value if v != self.null_value]
        field_name = self.to_field_name or "pk"
        print(self.queryset)
        print(value)
        result = list(self.queryset.filter(value__id__in=value).distinct())
        print(result)
        result += [self.null_value] if null else []
        print(result)
        return result


class CustomModelMultipleChoiceFilter(django_filters.ModelMultipleChoiceFilter):
    field_class = CustomField


class CustomFieldMptt(django_filters.fields.ModelMultipleChoiceField):
    def _check_values(self, value):
        null = self.null_label is not None and value and self.null_value in value
        if null:
            value = [v for v in value if v != self.null_value]
        field_name = self.to_field_name or "pk"
        result = list(
            self.queryset.filter(
                **{"{}__in".format(field_name): value}
            ).get_descendants(include_self=True)
        )
        result += [self.null_value] if null else []
        return result


class CustomModelMultipleChoiceFilterMptt(django_filters.ModelMultipleChoiceFilter):
    field_class = CustomFieldMptt


class ItemProductsFilter(django_filters.FilterSet):

    values = CustomModelMultipleChoiceFilter(
        field_name="attributes",
        to_field_name="id",
        queryset=AssignedProductAttributeValue.objects.all(),
        conjoined=False,
    )

    class Meta:
        model = Product
        fields = [
            "values",
        ]
