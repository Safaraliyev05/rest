from datetime import UTC
from random import choice, randint

import factory

from apps.models import Category, User, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('company')

    class Meta:
        model = Category

    @factory.lazy_attribute
    def parent(self):
        if Category.objects.exists():
            return choice(Category.objects.all())
        return None


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    last_login = factory.Faker('date_time', tzinfo=UTC)
    date_joined = factory.Faker('date_time', tzinfo=UTC)
    phone_number = factory.LazyAttribute(lambda self: '998' + self.phone_[4:])
    password = factory.django.Password('1')

    class Meta:
        model = User

    class Params:
        phone_ = factory.Faker('msisdn')

    @factory.lazy_attribute
    def balance(self):
        return randint(10, 100) * 1000

    @factory.lazy_attribute
    def type(self):
        return choice(User.Type.choices)[0]


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    price = factory.LazyAttribute(lambda self: randint(10, 100) * 1000)
    is_premium = factory.Faker('boolean')
    description = factory.Faker('text')
    category = factory.SubFactory(CategoryFactory)
    owner = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time', tzinfo=UTC)

    class Meta:
        model = Product
