import logging
import os
from logging.config import dictConfig

import sentry_sdk
from dotenv import load_dotenv
from opensearch_logger import OpenSearchHandler
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from test_task_anverali.conf.dev import DevelopmentConfig
from test_task_anverali.conf.logs import ExcludeBulkLogsFilter


load_dotenv()


LOGGING_CONFIG = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'json': {
            'format': '{"asctime": "%(asctime)s", "levelname": "%(levelname)s", "message": "%(message)s"}',
        },
        'raw': {'format': ''},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'filters': ['exclude_bulk_logs'],
        },
    },
    'filters': {
        'exclude_bulk_logs': {
            '()': ExcludeBulkLogsFilter,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


def initialize_logging():
    dictConfig(LOGGING_CONFIG)


def setup_sentry(node_config):
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
    sentry_sdk.init(
        dsn=node_config.SENTRY_SDK_DNS,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True,
        integrations=[FlaskIntegration(), sentry_logging]
    )


def setup_opensearch(node_config):
    logger = logging.getLogger("opensearch")
    handler = OpenSearchHandler(
        index_name="logs-index",
        hosts=[node_config.OPEN_SEARCH_URL],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def get_config():
    config_map = {
        'development': DevelopmentConfig,
        'tests': DevelopmentConfig,
    }

    environment = os.getenv('NODE_ENV', 'development')
    node_config = config_map.get(environment, DevelopmentConfig)
    initialize_logging()
    if node_config.SENTRY_ENABLED:
        setup_sentry(node_config)
    if node_config.OPEN_SEARCH_ENABLED:
        setup_opensearch(node_config)

    return node_config


config = get_config()
