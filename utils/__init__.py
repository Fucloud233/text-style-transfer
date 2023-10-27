import sys
sys.path.append(".")

from utils.config import Config

CONFIG_PATH = 'config.json'

# Config.set_config_info(read_config_info(CONFIG_PATH))
Config.load_config_info(CONFIG_PATH)