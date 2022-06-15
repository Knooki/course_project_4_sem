from django.test import TestCase

from applications.catalog.models import Category, Product


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):

        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data),'django')


class TestProductModel(TestCase):
    def setUp(self):
        self.data = Category.objects.create(name='django', slug='django')
        self.data1 = Product.objects.create(category=self.data, title='django', description='django', slug='django', price=38.3,is_active=False)
        
    def test_product_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data),'django')
       