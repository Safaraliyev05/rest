import pytest
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.reverse import reverse_lazy


@pytest.mark.django_db
class TestViews:
    def test_category(self, client, category):
        url = reverse_lazy('categories-list')
        response = client.get(url)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        data[0]['name'] = category.name

    # def test_product_list_with_pagination(self, client, products):
    #     page_size = 5
    #     url = reverse_lazy('product_list') + '?' + urlencode({'page_size': page_size})
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     response = response.json()
    #     assert len(response) == 4
    #     assert len(response['results']) == page_size
    #     assert response['previous'] is None
    #     next_page_url = reverse_lazy('product_list') + '?' + urlencode({'page': 2, 'page_size': page_size})
    #     assert next_page_url in response['next']
