import copy
from configs.settings import env_parameters
from typing import Dict
from tortoise import Tortoise


conn_mask = 'postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
config_mask = {
    'connections': {
        'default': ''
    },
    'apps': {
        'models': {
            'models': ['db.models'],
            'default_connection': 'default',
        }
    }
}

async def start(conn: Dict):
    await Tortoise.init(config=conn)
    await Tortoise.generate_schemas()


async def teardown():
    await Tortoise.close_connections()

def get_config(connection) -> Dict:
    config = copy.deepcopy(config_mask)
    config['connections']['default'] = connection
    return config


def get_connection():
    return conn_mask.format(
        DB_USERNAME=env_parameters.DB_USERNAME,
        DB_PASSWORD=env_parameters.DB_PASSWORD,
        DB_HOST=env_parameters.DB_HOST,
        DB_PORT=env_parameters.DB_PORT,
        DB_NAME=env_parameters.DB_NAME
    )
