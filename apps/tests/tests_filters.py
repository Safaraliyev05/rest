import pytest
from rest_framework import status
from rest_framework.reverse import reverse_lazy


@pytest.mark.django_db
class TestFilters:
    def test_max_min_price_filter(self, client, products):
        url = reverse_lazy('products-list')
        query = {
            'min_price': 50000
        }
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert product['price'] >= query['min_price']

        query = {
            'max_price': 100000
        }
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert product['price'] <= query['max_price']

    def test_owner_type_filter(self, client, products):
        query = {
            'owner_type': 'admin'
        }
        url = reverse_lazy('products-list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert product['user']['type'] == 'admin'

    def test_has_image_filter(self, client, products):
        url = reverse_lazy('products-list')
        response = client.get(url, {'has_image': True})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert product['images']

        # response = client.get(url, {'has_image': False})
        # assert response.status_code == status.HTTP_200_OK
        # data = response.json()
        # for product in data:
        #     assert len(product['images']) == 0

    def test_is_premium_filter(self, client, products):
        url = reverse_lazy('products-list')
        response = client.get(url, {'is_premium': True})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert product['is_premium']

        url = reverse_lazy('products-list')
        response = client.get(url, {'is_premium': False})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert not product['is_premium']

    def test_category_filter(self, client, products, category):
        url = reverse_lazy('products-list')
        response = client.get(url, {'category': category.id})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert product['category'] == category.id

    def test_search_product(self, client, products):
        url = reverse_lazy('products-list')
        key = 'hello'
        query = {
            'search': key
        }
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for product in data:
            assert key.lower() in product['name'].lower() or key.lower() in product['description'].lower()
