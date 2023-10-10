from rest_framework import status
from rest_framework.test import APITestCase

from webapp.products.models import Product
from webapp.products.tests.factories.product_factory import ProductFactory


# Constants for tests
URL = "/api/v1/products/"
CATEGORY = "category"
TEST_PRODUCT = "Test Product"
TEST_DESCRIPTION = "A test product"
NEXT = "next"
PREVIOUS = "previous"
TOTAL = "total"
IPHONE_PRO = "iPhone Pro"
ERGO_CHAIR = "Ergo Chair"
GALAXY = "Galaxy"
HUAWEI = "Huawei"
NAME = "name"
DESCRIPTION = "description"
PRICE = "price"
QUANTITY = "quantity"
RESULTS = "results"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
ID = "id"


class ProductViewSetTestCase(APITestCase):

    def setUp(self):
        self.product_data = {
            NAME: TEST_PRODUCT,
            DESCRIPTION: TEST_DESCRIPTION,
            PRICE: 100,
            QUANTITY: 10,
            CATEGORY: Product.ELECTRONICS
        }

        self.product = Product.objects.create(**self.product_data)

    def test_create_product(self):
        response = self.client.post(URL, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_product(self):
        invalid_product_data = {
            NAME: "",  # Missing name
            DESCRIPTION: "A test product without a name",
            PRICE: "-50.00",  # Negative price
            QUANTITY: "ten",  # Invalid quantity type
            CATEGORY: ""  # Missing category
        }

        response = self.client.post(URL, invalid_product_data)
        json_response = response.json()

        # The response should be a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", json_response)

        errors = json_response.get("errors")
        self.assertIn(NAME, errors)
        self.assertIn(QUANTITY, errors)
        self.assertIn(CATEGORY, errors)
        self.assertIn(PRICE, errors)

    def test_list_products(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()

        expected_response = {
            TOTAL: 1,
            NEXT: None,
            PREVIOUS: None,
            RESULTS: [
                {
                    ID: self.product.pk,
                    NAME: TEST_PRODUCT,
                    DESCRIPTION: TEST_DESCRIPTION,
                    QUANTITY: 10,
                    CATEGORY: Product.ELECTRONICS,
                    PRICE: "100.00"
                }
            ]
        }
        self.assertEqual(expected_response, json_response)

    def test_list_products_pagination(self):
        # Create 50 test products
        ProductFactory.create_batch(50)

        # Retrieve first page
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()

        self.assertIn(TOTAL, json_response)
        self.assertIn(NEXT, json_response)
        self.assertIn(PREVIOUS, json_response)
        self.assertEqual(len(json_response[RESULTS]), 25)

        # Retrieve next page
        response = self.client.get(json_response.get(NEXT))
        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(TOTAL, json_response)
        self.assertIn(NEXT, json_response)
        self.assertIn(PREVIOUS, json_response)
        self.assertEqual(len(json_response[RESULTS]), 25)

        # Retrieve previous page
        response = self.client.get(json_response.get(PREVIOUS))
        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(TOTAL, json_response)
        self.assertIn(NEXT, json_response)
        self.assertIn(PREVIOUS, json_response)
        self.assertEqual(len(json_response[RESULTS]), 25)

    def test_update_product(self):
        update_data = {
            NAME: "Updated Product",
            DESCRIPTION: "Updated test product",
            CATEGORY: Product.CLOTHING,
            QUANTITY: 5,
            PRICE: 100
        }
        response = self.client.put(f"{URL}{self.product.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, update_data[NAME])

    def test_invalid_update_product(self):
        update_data = {
            NAME: "Updated Product",
            DESCRIPTION: "Updated test product",
            CATEGORY: Product.CLOTHING,
            QUANTITY: -5,
            PRICE: 100
        }
        response = self.client.put(f"{URL}{self.product.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_product(self):
        partial_update_data = {
            NAME: "Partially Updated Product"
        }
        response = self.client.patch(
            f"{URL}{self.product.id}/", partial_update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, partial_update_data[NAME])

    def test_invalid_partial_update_product(self):
        partial_update_data = {
            QUANTITY: -100
        }
        response = self.client.patch(
            f"{URL}{self.product.id}/", partial_update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        response = self.client.delete(f"{URL}{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_delete_nonexistent_product(self):
        response = self.client.delete(f"{URL}12341234/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_produce(self):
        response = self.client.get(f"{URL}{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()
        expected_response = {
            ID: self.product.pk,
            NAME: TEST_PRODUCT,
            DESCRIPTION: TEST_DESCRIPTION,
            QUANTITY: 10,
            CATEGORY: Product.ELECTRONICS,
            PRICE: '100.00'
        }
        self.assertEqual(json_response, expected_response)

    def test_retrieve_invalid_product(self):
        response = self.client.get(f"{URL}12341234/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProductFilterTestCase(APITestCase):

    def setUp(self):
        ProductFactory.create(name=IPHONE_PRO,
                              price=1000.00, category=Product.ELECTRONICS)
        ProductFactory.create(name=GALAXY, price=800.00,
                              category=Product.FOOD)
        ProductFactory.create(
            name=ERGO_CHAIR, price=150.00, category=Product.CLOTHING)
        ProductFactory.create(
            name=HUAWEI, price=150.00, category=Product.ELECTRONICS)

    def test_filter_min_price(self):
        response = self.client.get(URL, {MIN_PRICE: 900})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[RESULTS]), 1)
        self.assertEqual(response.data[RESULTS][0][NAME], IPHONE_PRO)

    def test_filter_max_price(self):
        response = self.client.get(URL, {MAX_PRICE: 200})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[RESULTS]), 2)
        self.assertEqual(response.data[RESULTS][0][NAME], ERGO_CHAIR)

    def test_filter_category(self):
        response = self.client.get(URL, {CATEGORY: Product.CLOTHING})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[RESULTS]), 1)
        self.assertEqual(response.data[RESULTS][0][NAME], ERGO_CHAIR)

    def test_filter_combined(self):
        response = self.client.get(
            URL, {NAME: GALAXY, MIN_PRICE: 200, MAX_PRICE: 900, CATEGORY: Product.FOOD})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[RESULTS]), 1)
        self.assertEqual(response.data[RESULTS][0][NAME], GALAXY)
