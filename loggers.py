import json
import logging
import logging.config

from config import settings

bot = logging.getLogger('bot')


def setup():
    dict_config = json.load(open(settings.LOGGING_CONF_FILE, 'r'))
    logging.config.dictConfig(
        config=dict_config
    )
