from random import choice, randint

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from apps.models import Category, User, Product, Favourite


class Command(BaseCommand):
    help = "Seed database with sample data for app.models"

    def add_arguments(self, parser):
        parser.add_argument('-c', '--category', type=int, help="Number of categories to seed")
        parser.add_argument('-u', '--user', type=int, help="Number of users to seed")
        parser.add_argument('-p', '--product', type=int, help="Number of products to seed")
        parser.add_argument('-f', '--favourite', type=int, help="Number of favourites to seed")

    def _category(self, n: int):
        f = Faker()
        for _ in range(n):
            Category.objects.create(name=f.company())
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} categories."))

    def _user(self, n: int):
        f = Faker()
        user_list = []
        for _ in range(n):
            user_list.append(User(
                first_name=f.first_name(),
                last_name=f.last_name(),
                username=f.user_name(),
                type=choice(User.Type.choices)[0],
                balance=randint(100, 5000) * 1000,
                password=make_password(f.password(5)),
                email=f.email()
            ))
        User.objects.bulk_create(user_list)
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} users."))

    def _product(self, n: int):
        f = Faker()
        products_list = []
        categories = list(Category.objects.values_list('id', flat=True))
        users = list(User.objects.values_list('id', flat=True))
        for _ in range(n):
            products_list.append(Product(
                name=f.color_name() + " " + f.word().capitalize(),
                price=randint(1000, 100000),
                description=f.text(),
                is_premium=choice([True, False]),
                created_at=f.date_time(),
                category_id=choice(categories),
                owner_id=choice(users)
            ))
        Product.objects.bulk_create(products_list)
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} products."))

    def _favourite(self, n: int):
        f = Faker()
        favourite_list = []
        users = list(User.objects.values_list('id', flat=True))
        products = list(Product.objects.values_list('id', flat=True))
        for _ in range(n):
            favourite_list.append(Favourite(
                created_at=f.date_time(),
                owner_id=choice(users),
                product_id=choice(products)
            ))
        Favourite.objects.bulk_create(favourite_list)
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} favourites."))

    def handle(self, *args, **options):
        if options['category']:
            self._category(options['category'])
        if options['user']:
            self._user(options['user'])
        if options['product']:
            self._product(options['product'])
        if options['favourite']:
            self._favourite(options['favourite'])

        self.stdout.write(self.style.SUCCESS("Successfully added data to the database."))
