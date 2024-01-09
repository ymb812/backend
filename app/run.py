import uvicorn
from configs.settings import env_parameters
from setup import app

if __name__ == '__main__':
    uvicorn.run(app, host=env_parameters.REST_HOST, port=env_parameters.REST_PORT)
