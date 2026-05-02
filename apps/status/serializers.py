from rest_framework import serializers


class ProductSwaggerSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    image = serializers.SerializerMethodField()

    title = serializers.CharField()
    description = serializers.CharField()
    slug = serializers.CharField()

    regular_price = serializers.CharField()
    card_price = serializers.CharField(allow_null=True)
    discount_percent = serializers.CharField(allow_null=True)

    brand = serializers.CharField()
    country = serializers.CharField()
    weight = serializers.CharField()
    stock = serializers.IntegerField()
    is_available = serializers.BooleanField()

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    seller = serializers.IntegerField()
    catgories = serializers.IntegerField()

    def get_image(self, obj):
        request = self.context.get("request")

        if not obj.image:
            return None

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url

class OrderItemSwaggerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = ProductSwaggerSerializer()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()


class OrderSwaggerSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    full_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    house = serializers.CharField()
    apartment = serializers.CharField()
    comment = serializers.CharField()

    total_price = serializers.FloatField()
    status = serializers.CharField()

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    items = OrderItemSwaggerSerializer(many=True)



class StatsSwaggerSerializer(serializers.Serializer):
    today_balance = serializers.FloatField()
    today_growth_percent = serializers.FloatField()

    new_orders = serializers.IntegerField()
    today_orders_growth = serializers.FloatField()

    total_products = serializers.IntegerField()
    low_stock_count = serializers.IntegerField()

    average_rating = serializers.FloatField()
    rating_growth = serializers.FloatField()


class WeeklySalesSwaggerSerializer(serializers.Serializer):
    day = serializers.CharField()
    total = serializers.FloatField()



class TaskSwaggerSerializer(serializers.Serializer):
    title = serializers.CharField()
    time = serializers.CharField()
    status = serializers.CharField()
    priority = serializers.CharField()



class SellerDashboardSwaggerSerializer(serializers.Serializer):
    stats = StatsSwaggerSerializer()
    recent_orders = OrderSwaggerSerializer(many=True)
    weekly_sales = WeeklySalesSwaggerSerializer(many=True)
    tasks = TaskSwaggerSerializer(many=True)