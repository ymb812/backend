from tortoise import fields
from tortoise.models import Model
import api.schemas.v1.web_user as v1_web_user
import api.schemas.v1.web_shop as v1_web_shop
import api.schemas.v1.product as v1_product


class Client(Model):
    class Meta:
        table = 'clients'

    uuid = fields.UUIDField(pk=True)
    user_id = fields.BigIntField(index=True)  # get from bot_manager
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid', null=True)


class WebUser(Model):
    class Meta:
        table = 'users'
        ordering = ['created_at']

    uuid = fields.UUIDField(pk=True)
    email = fields.CharField(unique=True, max_length=255)
    password = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def update_fields(self, updated_fields: v1_web_user.WebUserToBeUpdatedModel):
        for field, value in updated_fields.model_dump().items():
            if value is not None:
                setattr(self, field, value)

        await self.save()

class Seller(Model):
    class Meta:
        table = 'sellers'
        ordering = ['created_at']

    uuid = fields.ForeignKeyField(model_name='models.WebUser', to_field='uuid', pk=True)
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid', related_name='sellers_by_shop',
                                      null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Admin(Model):
    class Meta:
        table = 'admins'
        ordering = ['created_at']

    uuid = fields.ForeignKeyField(model_name='models.WebUser', to_field='uuid', pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class WebShop(Model):
    class Meta:
        table = 'web_shops'
        ordering = ['created_at']

    uuid = fields.UUIDField(pk=True)
    name = fields.TextField()
    bot_id = fields.BigIntField(unique=True)  # get from bot_manager
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def update_fields(self, updated_fields: v1_web_shop.WebShopToBeUpdatedModel):
        for field, value in updated_fields.model_dump().items():
            if value is not None:
                setattr(self, field, value)

        await self.save()


class Product(Model):
    class Meta:
        table = 'products'

    uuid = fields.UUIDField(pk=True)
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid')
    article = fields.CharField(max_length=255, null=True)
    name = fields.TextField(null=True)
    description = fields.CharField(max_length=4096)
    discount_percent = fields.FloatField(default=0)
    category = fields.ForeignKeyField(model_name='models.Category', to_field='uuid')
    media_data = fields.TextField(null=True)
    order_priority = fields.BigIntField(default=0)

    async def update_fields(self, updated_fields: v1_product.ProductToBeUpdatedModel):
        for field, value in updated_fields.model_dump().items():
            if value is not None:
                setattr(self, field, value)

        await self.save()


class Category(Model):
    class Meta:
        table = 'categories'

    uuid = fields.UUIDField(pk=True)
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid')
    title = fields.CharField(max_length=140, null=False)
    order_priority = fields.SmallIntField(null=False)
    # Composite PK - order and web_shop - ???зачем на ордер???


class ProductPrice(Model):
    class Meta:
        table = 'products_prices'

    uuid = fields.UUIDField(pk=True)
    product = fields.ForeignKeyField(model_name='models.Product', to_field='uuid')
    currency = fields.CharField(max_length=8)
    amount = fields.FloatField()  # price
    discount_percent = fields.FloatField(null=True)


#idk
class CartItems(Model):
    class Meta:
        table = 'carts_items'

    cart = fields.ForeignKeyField(model_name='models.Cart', to_field='uuid', related_name='products_by_cart')
    product = fields.ForeignKeyField(model_name='models.Product', to_field='uuid')
    # color ?
    # size ?
    amount = fields.IntField(default=1, null=False)

    # Composite PK - cart, product, color, size


# idk
class Cart(Model):
    class Meta:
        table = 'carts'

    uuid = fields.UUIDField(pk=True)
    order = fields.ForeignKeyField(model_name='models.Order', to_field='uuid', null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


# idk
class Order(Model):
    class Meta:
        table = 'orders'

    uuid = fields.UUIDField(pk=True)
    client = fields.ForeignKeyField(model_name='models.Client', to_field='uuid')
    status = fields.JSONField(null=True)
    delivery_data = fields.JSONField(null=True)
    paid_data = fields.JSONField(null=True)
    paid_at = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class RefLink(Model):
    class Meta:
        table = 'ref_links'

    uuid = fields.UUIDField(pk=True)
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid', related_name='ref_links_by_shop')
    link = fields.CharField(max_length=256, unique=True)
    creator = fields.ForeignKeyField(model_name='models.Client', to_field='uuid')
    payload = fields.TextField()
    # is_for_catalog = fields.BooleanField()
    # is_for_bot = fields.BooleanField()
    # is_for_product = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)


class PromoCode(Model):
    class Meta:
        table = 'promo_codes'

    uuid = fields.UUIDField(pk=True)
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid', related_name='promocodes_by_shop')
    name = fields.TextField(null=True)
    discount_percent = fields.FloatField(default=0)  # percent or amount
    discount_price = fields.FloatField(default=0)  # percent or amount
    valid_from = fields.DatetimeField()
    valid_until = fields.DatetimeField()
    valid_number_of_uses = fields.BigIntField(null=True)
    valid_from_price = fields.FloatField(default=0)
    is_valid_for_discount_products = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)


class Mailing(Model):
    class Meta:
        table = 'mailings'

    uuid = fields.UUIDField(pk=True)
    web_shop = fields.ForeignKeyField(model_name='models.WebShop', to_field='uuid', related_name='mailings_by_shop')
    recipients_amount = fields.BigIntField(default=0)
    text = fields.TextField(null=True)
    photo = fields.TextField(null=True)
    required_orders_amount = fields.BigIntField(default=0)
    inline_text = fields.TextField()
    inline_link = fields.TextField(null=True)
    starts_at = fields.DatetimeField()
    ends_at = fields.DatetimeField(null=True)  # when mailing ends we set as datetime.now()
