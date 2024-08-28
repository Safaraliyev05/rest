from datetime import timedelta

from django.db.models import Count, F
from django.utils import timezone
from django_filters import FilterSet, CharFilter, BooleanFilter, ChoiceFilter, NumberFilter

from apps.models import Product, Category, User


class ProductFilterSet(FilterSet):
    category = CharFilter(method='filter_by_category')
    has_image = BooleanFilter(method='has_image_filter')
    owner_type = ChoiceFilter(method='owner_filter', choices=User.Type.choices)
    days = NumberFilter(method='days_filter')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    equal_count = BooleanFilter(method='equal_product_favourite_count')

    class Meta:
        model = Product
        fields = ('is_premium',)

    def filter_by_category(self, queryset, field, value):
        matching_categories = Category.objects.filter(name__icontains=value)
        child_categories = Category.objects.filter(parent__in=matching_categories)

        return queryset.filter(
            category__in=list(matching_categories) + list(child_categories)
        )

    def days_filter(self, queryset, name, value):
        return queryset.filter(created_at__gte=timezone.now() - timedelta(days=int(value)))

    def has_image_filter(self, queryset, name, value):
        if value:
            return queryset.annotate(image_count=Count('images')).filter(image_count__gt=0)
        return queryset

    def owner_filter(self, queryset, name, value):
        return queryset.filter(owner__type=value)

    def equal_product_favourite_count(self, queryset, name, value):
        if value:
            # Users with equal product and favourite count
            users_with_equal_count = User.objects.annotate(
                product_count=Count('product'),
                favourite_count=Count('favourite')
            ).filter(product_count=F('favourite_count')).values('id')

            return queryset.filter(owner__id__in=users_with_equal_count)
        return queryset
