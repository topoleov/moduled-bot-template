from core.utils import get_config
import os

# path settings (logs, screenshots, downloads, databases)

ROOT = os.path.join(os.path.dirname(__file__))  # корневая директория
yaml_config = get_config(os.path.join(ROOT, "config.yaml")) # config.yaml file
LOG_DIR = os.path.join(ROOT, "log")
SCREENSHOT_DIR = os.path.join(ROOT, "screenshots")
DOWNLOADS_DIR = os.path.join(ROOT, "downloads")

# SQL settings

DATABASE_NAME = yaml_config.get("db").get("name")
DATABASE_TEST_NAME = yaml_config.get("db").get("name")
DATABASE_USERNAME = yaml_config.get("db").get("username")
DATABASE_PASSWORD = yaml_config.get("db").get("password")
DATABASE_HOST = yaml_config.get("db").get("host")
DATABASE_PORT = yaml_config.get("db").get("port")
DATABASE_HOST_TEST = yaml_config.get("db").get("host_test")
DATABASE_PORT_TEST = yaml_config.get("db").get("port_test")

# Mattermost settings | optional block

MATTERMOST_ID = yaml_config.get("mattermost").get("id")
MATTERMOST_TOKEN = yaml_config.get("mattermost").get("token")

MATTERMOST_HTTP_HOST = yaml_config.get("mattermost").get("http_host").rstrip('/')
MATTERMOST_API_LOCATION = yaml_config.get("mattermost").get("api_location").rstrip('/')
MATTERMOST_API_VERSION = yaml_config.get("mattermost").get("api_version")
MATTERMOST_WS_URL = yaml_config.get("mattermost").get("ws_url").rstrip('/')

MATTERMOST_FILTER_MESSAGES_CONTAINS = yaml_config.get("mattermost").get("filter_messages_contains")
MATTERMOST_LISTEN_CHANNELS = yaml_config.get("mattermost").get("listen_channels")
MATTERMOST_TARGET_EVENTS = yaml_config["mattermost"]["target_events_processors"]
