from rest_framework import status

from arcgis_marketplace import factories
from ...views import BaseViewTests


class ProductViewTests(BaseViewTests):

    def test_product_list_200_OK(self):
        response = self.client.get(self.reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_201_CREATED(self):
        product = factories.ItemFactory.build()
        response = self.client.post(self.reverse('product-list'), {
            'title': product.title,
            'price': int(product.price)
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], product.title)

    def test_product_create_400_BAD_REQUEST(self):
        product = factories.ItemFactory.build()
        response = self.client.post(self.reverse('product-list'), {
            'title': product.title,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_detail_200_OK(self):
        product = factories.ItemFactory(owner=self.account)
        response = self.client.get(product.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], product.id.hex)

    def test_product_update_200_OK(self):
        product = factories.ItemFactory(owner=self.account)
        response = self.client.patch(
            product.get_absolute_url(), {
                'title': 'updated'
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'updated')

    def test_product_delete_204_NO_CONTENT(self):
        product = factories.ItemFactory(owner=self.account)
        response = self.client.delete(product.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
