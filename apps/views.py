from random import randint

from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from apps.filters import ProductFilterSet
from apps.models import Category, Product, Favourite
from apps.models import User
from apps.serializers import CategoryModelSerializer, ProductListModelSerializer, FavouriteModelSerializer, \
    EmailModelSerializer, VerifyEmailSerializer
from apps.tasks import send_to_email


@extend_schema(tags=['category'])
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['product'])
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilterSet
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']  # default


@extend_schema(tags=['favourites'])
class FavouriteListCreateAPIView(ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteModelSerializer


class SendEmailAPIView(GenericAPIView):
    serializer_class = EmailModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        username = serializer.data['username']

        code = randint(1000, 9999)
        cache.set(email, {'code': code, 'username': username}, timeout=120)

        message = f"Your verification code is {code}"
        # send_to_email(message, email)
        send_to_email.delay(message, email)

        email = serializer.data['email']
        code = randint(1000, 9999)
        cache.set(email, code, timeout=120)

        message = f"Your verification code is {code}"
        send_to_email(message, email)

        print(f"Email: {email}, code: {code}")
        return Response({"message": "Code sent successfully"})


class VerifyEmailAPIView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        code = serializer.data['code']

        cached_data = cache.get(email)

        cached_code = cached_data.get('code')
        username = cached_data.get('username')

        if code != cached_code:
            raise ValidationError('Code is incorrect.')

        user = User.objects.filter(email=email).first()
        if user is None:
            user = User.objects.create(email=email, username=username)
            user.save()

        return Response({"message": "User added successfully"})
