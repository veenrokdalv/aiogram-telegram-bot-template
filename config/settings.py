from pathlib import Path

from environ import Env

BASE_DIR = Path(__name__).resolve().parent

ENV_FILE = BASE_DIR / '.env'
LOGGING_CONF_FILE = BASE_DIR / 'logging.conf.json'

env = Env()

env.read_env(str(ENV_FILE))

TELEGRAM_BOT_TOKENS = env.list('TELEGRAM_BOT_TOKENS')
PARSE_MODE = 'HTML'

del env
