from pathlib import Path
from zoneinfo import ZoneInfo

from environ import Env

BASE_DIR = Path(__name__).resolve().parent

ENV_FILE = BASE_DIR / '.env'
LOGGING_CONF_FILE = BASE_DIR / 'logging.conf.json'

env = Env()
env.read_env(str(ENV_FILE))

PARSE_MODE = 'HTML'
THROTTLING_KEY = '_throttling_key'
TELEGRAM_BOT_TOKENS = env.list('TELEGRAM_BOT_TOKENS')
DEFAULT_TIME_ZONE = ZoneInfo('Europe/Moscow')

SHORT_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

THROTTLES = {
    'default': '5/1s'  # 5 messages per second
}

del env
