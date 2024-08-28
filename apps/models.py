from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, IntegerField, DateTimeField, TextField, ForeignKey, CASCADE, ImageField, \
    TextChoices, BooleanField, SET_NULL, UniqueConstraint
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    class Type(TextChoices):
        MODERATOR = 'moderator', 'Moderator'
        MANAGER = 'manager', 'Manager'
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    type = CharField(max_length=10, choices=Type.choices, default=Type.USER)
    balance = IntegerField(db_default=0)
    phone_number = CharField(max_length=255, unique=True)

    # USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number


class Category(MPTTModel):
    name = CharField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    description = TextField(null=True, blank=True)
    category = ForeignKey('Category', SET_NULL, null=True, blank=True)
    owner = ForeignKey('User', CASCADE)
    is_premium = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Favourite(Model):
    owner = ForeignKey('User', CASCADE)
    product = ForeignKey('Product', CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['owner', 'product'], name='unique_favourite')
        ]


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d/')
    product = ForeignKey('Product', CASCADE, related_name='images')
