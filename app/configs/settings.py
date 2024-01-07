import logging
import os
import sys

from dotenv import load_dotenv
from pydantic import ValidationError

from configs.env_configs_models import EnvConfigsModel

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
root_logger = logging.getLogger()
_logger = logging.getLogger(__name__)

# This flag available only in production enviroment
is_prod = os.environ.get('PROD_MODE') in [1, True, 'true', 'True']

if is_prod:
    root_logger.setLevel(logging.INFO)
else:
    root_logger.setLevel(logging.INFO)
    load_dotenv(dotenv_path=os.path.join('configs', '.env'))

try:
    env_parameters = EnvConfigsModel(**os.environ)
except ValidationError as e:
    _logger.critical(exc_info=e, msg='Env parameters validation')
    sys.exit(-1)
