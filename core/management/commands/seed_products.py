from django.core.management.base import BaseCommand
from apps.catalog.models import Product, Category
from apps.users.models import SellerProfile
from django.utils.text import slugify
import uuid


class Command(BaseCommand):
    help = "Seed products"

    def handle(self, *args, **kwargs):
        seller = SellerProfile.objects.first()
        category = Category.objects.first()

        if not seller or not category:
            self.stdout.write(self.style.ERROR("❌ Seller yoki Category yo‘q"))
            return

        # 🔥 eski productlarni tozalash (ixtiyoriy, lekin tavsiya qilaman)
        Product.objects.all().delete()

        products = [ 
            { 
                "title": "Блинчики с мясом", 
                "brand": "Домашние", 
                "country": "Россия", 
                "regular_price": 50.50, 
                "card_price": 44.50, 
                "discount_percent": 50, 
                "weight": "500 г", 
                "image": "order/shirinlik.png", 
            }, 
            { 
                "title": "Молоко Простоквашино", 
                "brand": "Простоквашино", 
                "country": "Россия", 
                "regular_price": 50.50, 
                "card_price": 44.50, 
                "discount_percent": 50, 
                "weight": "1 л", 
                "image": "order/sut.png", 
            }, 
            { 
                "title": "Колбаса сырокопченая", 
                "brand": "Мясная история", 
                "country": "Россия", 
                "regular_price": 50.50, 
                "card_price": 44.50, 
                "discount_percent": 50, 
                "weight": "300 г", 
                "image": "order/qadoqliKolbosa.png", 
            },
            { 
                "title": "Сосиски вареные", 
                "brand": "Мясная история", 
                "country": "Россия", 
                "regular_price": 50.50, 
                "card_price": 44.50, 
                "discount_percent": 50, 
                "weight": "400 г", 
                "image": "order/qadoqliSosiska.png", 
            },
            { 
                "title": "Колбаса салями", 
                "brand": "Десна", 
                "country": "Беларусь", 
                "regular_price": 599.99, 
                "card_price": None, 
                "discount_percent": None, 
                "weight": "700 г", 
                "image": "order/Pasted_image.png", 
            },
            { 
                "title": "Комбайн КЗС-1218 «ДЕСНА-ПОЛЕСЬЕ GS12»", 
                "brand": "ГОСТ", 
                "country": "Россия", 
                "regular_price": 159.99, 
                "card_price": None, 
                "discount_percent": None, 
                "weight": "500 г", 
                "image": "order/indeyka.png", 
            },
            { 
                "title": "Молоко сгущенное РОГАЧЕВ Егорка, цельное с сахаром...", 
                "brand": "ГОСТ", 
                "country": "Россия", 
                "regular_price": 140.21, 
                "card_price": 69.99, 
                "discount_percent": 20, 
                "weight": "500 г", 
                "image": "order/krem.png", 
            },
            { 
                "title": "Масло сливочное ПРОСТОКВАШИНО 82.5%", 
                "brand": "ГОСТ", 
                "country": "Россия", 
                "regular_price": 192.99, 
                "card_price": None, 
                "discount_percent": None, 
                "weight": "500 г", 
                "image": "order/yog.png", 
            },
        ]

        for item in products:
            base_slug = slugify(item["title"])

            # 🔥 agar slug bo‘sh chiqsa
            if not base_slug:
                base_slug = "product"

            # 🔥 unique slug
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

            Product.objects.create(
                seller=seller,
                catgories=category,
                title=item["title"],
                description=f"{item['title']} - высокое качество",
                slug=unique_slug,
                regular_price=item["regular_price"],
                card_price=item["card_price"],
                discount_percent=item["discount_percent"],
                image=item['image'],
                brand=item["brand"],
                country=item["country"],
                weight=item["weight"],
                stock=100,
                is_available=True,
            )

        self.stdout.write(self.style.SUCCESS("✅ Products created!"))