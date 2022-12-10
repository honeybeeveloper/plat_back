from config.config import Config
from config.logging import get_logger

app_config = Config(config_file='config.json')
app_logger = get_logger('ozz_backend', app_config)
print(app_config)
