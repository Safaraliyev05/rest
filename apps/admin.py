from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mptt.admin import DraggableMPTTAdmin

from apps.models import Category, Product, ProductImage, User, Favourite


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    extra = 2
    min_num = 0


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageStackedInline]
    list_display = 'name', 'category'


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'balance']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone_number", "password1", "password2", "balance", "email"),
            },
        ),
    )


@admin.register(Favourite)
class FavouriteModelAdmin(admin.ModelAdmin):
    pass
