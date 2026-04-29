from datetime import date, timedelta

from django.db.models import Sum, Avg
from django.db.models.functions import TruncDate

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product
from apps.reviews.models import Review
from apps.status.models import Tasks
from ..catalog.permissions import IsSellerOrReadOnly
from .serializers import SellerDashboardSwaggerSerializer

class SellerDashboardView(APIView):
    permission_classes = [IsSellerOrReadOnly]
    
    @extend_schema(
      responses=SellerDashboardSwaggerSerializer
    )
    def get(self, request):
        user = request.user
        seller = user.sellerprofile

        today = date.today()
        yesterday = today - timedelta(days=1)

        # =========================
        # 🔥 ORDERS FILTER (FIXED RELATED NAME)
        # =========================
        today_orders = Order.objects.filter(
            order_items__product__seller=seller,
            created_at=today
        ).distinct()

        yesterday_orders = Order.objects.filter(
            order_items__product__seller=seller,
            created_at=yesterday
        ).distinct()

        # =========================
        # 💰 BALANCE
        # =========================
        today_balance = today_orders.aggregate(total=Sum("total_price"))["total"] or 0
        yesterday_balance = yesterday_orders.aggregate(total=Sum("total_price"))["total"] or 0

        growth_percent = 0
        if yesterday_balance:
            growth_percent = round(
                ((today_balance - yesterday_balance) / yesterday_balance) * 100,
                2
            )

        # =========================
        # 📦 NEW ORDERS (ITEM COUNT)
        # =========================
        new_orders = OrderItem.objects.filter(
            product__seller=seller,
            order__created_at=today
        ).aggregate(total=Sum("quantity"))["total"] or 0

        # =========================
        # 🛍 PRODUCTS
        # =========================
        products = Product.objects.filter(seller=seller)

        total_products = products.count()
        low_stock_count = products.filter(stock__lte=5).count()

        # =========================
        # ⭐ RATING
        # =========================
        rating = Review.objects.filter(
            product__seller=seller
        ).aggregate(avg=Avg("rating"))["avg"] or 0

        # =========================
        # 📦 RECENT ORDERS (FULL STRUCTURE)
        # =========================
        recent_orders_qs = Order.objects.filter(
            order_items__product__seller=seller
        ).prefetch_related(
            "order_items__product"
        ).order_by("-created_at").distinct()[:5]

        recent_orders = []
        for order in recent_orders_qs:
            items = []

            for item in order.order_items.all():
                product = item.product

                items.append({
                    "id": item.id,
                    "product": {
                        "id": product.id,
                        "image": request.build_absolute_uri(product.image.url) if product.image else None,
                        "title": product.title,
                        "description": product.description,
                        "slug": product.slug,
                        "regular_price": str(product.regular_price),
                        "card_price": str(product.card_price) if product.card_price else None,
                        "discount_percent": str(product.discount_percent) if product.discount_percent else None,
                        "brand": product.brand,
                        "country": product.country,
                        "weight": product.weight,
                        "stock": product.stock,
                        "is_available": product.is_available,
                        "created_at": product.created_at,
                        "updated_at": product.updated_at,
                        "seller": product.seller_id,
                        "catgories": product.catgories_id
                    },
                    "quantity": item.quantity,
                    "price": item.price
                })

            recent_orders.append({
                "id": order.id,
                "full_name": order.full_name,
                "phone": order.phone,
                "address": order.address,
                "house": order.house,
                "apartment": order.apartment,
                "comment": order.comment,
                "total_price": order.total_price,
                "status": order.status,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "items": items
            })

        # =========================
        # 📊 WEEKLY SALES
        # =========================
        last_7_days = today - timedelta(days=6)

        weekly_sales_qs = Order.objects.filter(
            order_items__product__seller=seller,
            created_at__gte=last_7_days
        ).annotate(day=TruncDate("created_at")) \
         .values("day") \
         .annotate(total=Sum("total_price")) \
         .order_by("day")

        weekly_sales = [
            {
                "day": item["day"].strftime("%a"),
                "total": item["total"]
            }
            for item in weekly_sales_qs
        ]

        # =========================
        # 🧠 TASKS
        # =========================
        tasks_qs = Tasks.objects.filter(seller=seller).order_by("-time")[:5]

        tasks = [
            {
                "title": t.title,
                "time": t.time.strftime("%H:%M"),
                "status": t.status,
                "priority": t.priority
            }
            for t in tasks_qs
        ]

        # =========================
        # ✅ RESPONSE
        # =========================
        return Response({
            "stats": {
                "today_balance": today_balance,
                "today_growth_percent": growth_percent,
                "new_orders": new_orders,
                "today_orders_growth": 0,
                "total_products": total_products,
                "low_stock_count": low_stock_count,
                "average_rating": round(rating, 1),
                "rating_growth": 0
            },
            "recent_orders": recent_orders,
            "weekly_sales": weekly_sales,
            "tasks": tasks
        })
    # frontend_data = {
    #   "stats": {
    #     "today_balance": 4280,
    #     "today_growth_percent": 12,

    #     "new_orders": 12,
    #     "today_orders_growth": 3,

    #     "total_products": 48,
    #     "low_stock_count": 2,

    #     "average_rating": 4.8,
    #     "rating_growth": 0.2
    #   },

    #   "recent_orders": [
    #     {
    #       "id": 2482,
    #       "code": "ORD-2482",
    #       "product_name": "Qora futbolka XL",
    #       "quantity": 2,
    #       "total_price": 85000,
    #       "status": "new",
    #       "created_at": "2026-04-25T10:00:00"
    #     }
    #   ],

    #   "weekly_sales": [
    #     {
    #       "day": "Mon",
    #       "total": 120000
    #     },
    #     {
    #       "day": "Tue",
    #       "total": 90000
    #     }
    #   ],

    #   "tasks": [
    #     {
    #       "title": "Yangi mahsulot qo‘shish",
    #       "time": "09:00",
    #       "status": "done",
    #       "priority": "high"
    #     }
    #   ]
    # }
    

class AdminDashboardView(APIView):
  def get(self, request):
    return Response({"ok": "ok"})


class AdminProductsView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class SellerProductsView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class AdminOrdersView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class SellerOrdersView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class AdminCategoriesView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class SellerCategoriesView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class AdminStatisticsView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class SellerStatisticsView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class AdminAdminToolsView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})


class NotificationsView(APIView):
  def get(self, requeast):
    return Response({"ok": "ok"})
