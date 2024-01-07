from fastapi.testclient import TestClient
from core.webhooks.models import *
from core.webhooks import app
import uuid

client = TestClient(app)


def test_creating():
    response = client.post('/product', json=ProductModel(
        uuid='5624a04b-4a50-4399-8896-b30f340194a7',
        web_shop_uuid='5624a04b-4a50-4399-8896-b30f340194a6',
        article='1',
        name='test',
        description='desc',
        discount_percent=0,
        category_uuid='5624a04b-4a50-4399-8896-b30f340194a6',
        media_data='media_data',
        order_priority=999
    ).model_dump(), headers={'auth-token': 'qwerty'}
                           )

    assert response.status_code == 200
