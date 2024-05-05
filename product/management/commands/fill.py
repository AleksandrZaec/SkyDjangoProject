import json
from django.core.management import BaseCommand
from product.models import Product, Category


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open('product.json', 'r', encoding='utf-8') as data_file:
#             products = json.load(data_file)
#             for product in products:
#                 category_id = product['fields']['category']
#                 category = Category.objects.get(product_name=category_id)
#                 product_instance = Product(
#                     product_name=product['fields']['product_name'],
#                     description=product['fields']['description'],
#                     category=category,
#                     unit_price=product['fields']['unit_price']
#                 )
#                 product_instance.save()

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open('product.json', 'r', encoding='utf-8') as data_file:
#             products = json.load(data_file)
#             for product in products:
#                 category_id = product['fields']['category']
#                 category = Category.objects.get(product_name=category_id)
#                 product_instance = Product(
#                     product_name=product['fields']['product_name'],
#                     description=product['fields']['description'],
#                     category=category,
#                     unit_price=product['fields']['unit_price']
#                 )
#                 product_instance.save()
class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete()
        with open('product.json', 'r', encoding='utf-8') as data_file:
            products = json.load(data_file)
            for product in products:
                Product.objects.create(
                    product_name=product['product_name'],
                    description=product['description'],
                    category_id=product['category'],
                    unit_price=product['unit_price']
                )

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены в базу данных'))