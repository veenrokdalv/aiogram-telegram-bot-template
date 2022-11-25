from pathlib import Path

from environ import Env

BASE_DIR = Path(__name__).resolve().parent

# config env file
ENV_FILE = BASE_DIR / '.env'

# logging config file
LOGGING_CONF_FILE = BASE_DIR / 'logging.conf.json'

_env = Env()
_env.read_env(str(ENV_FILE))

# I18n
LOCALES_DIR = BASE_DIR / 'locales'
I18N_DOMAIN = 'bot'

DEFAULT_LANGUAGE_CODE = 'ru'

# Bot settings
TELEGRAM_BOT_TOKENS = _env.list('TELEGRAM_BOT_TOKENS')
PARSE_MODE = 'HTML'

# Throttle settings
THROTTLING_KEY = '_throttling_key'
THROTTLES = {
    'default': '5/1s'  # 5 messages per second
}
