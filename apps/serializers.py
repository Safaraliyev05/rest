from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Category, Product, User, ProductImage, Favourite


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'type'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageModelSerializer(ModelSerializer):
    image = ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = 'id', 'image'


class FavouriteModelSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['user'] = UserModelSerializer(instance.owner).data
        repr['images'] = ProductImageModelSerializer(instance.images, many=True, context=self.context).data
        return repr


class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['category'] = CategoryModelSerializer(instance.category).data
        return repr


class EmailModelSerializer(Serializer):
    email = CharField(max_length=255)
    username = CharField(max_length=150)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return attrs


class VerifyEmailSerializer(Serializer):
    email = CharField(max_length=255, default='uzblordsardorboy0705@gmail.com')
    code = IntegerField(default=4444)

    def validate(self, attrs: dict):
        email = attrs.get('email')
        code = attrs.get('code')
        cache_code = cache.get(email)
        print(f"Email: {email}, Code: {code}, Cached Code: {cache_code}")
        if code != cache_code.get('code'):
            raise ValidationError('Code is incorrect')
        if code != cache_code:
            raise ValidationError('Code eskirgan')
        return attrs
