import os
from datetime import datetime, timezone
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# SYSTEM
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
ADMIN_EMAIL = os.getenv("ENV_VAR_ADMIN_EMAIL")

# DATA
LOG_PATH = f"{BASE_DIR}/logs/"
DATA_PATH = f"{BASE_DIR}/data/"
MEXC_DATA_PATH = f"{BASE_DIR}/data/mexc/"

# DWH
DWH_CONN_STR = os.getenv("ENV_VAR_DWH_CONN_STR")

# SNOOPY TELEGRAM BOT
SNOOPY_BOT_LINK = os.getenv("ENV_VAR_SNOOPY_BOT_LINK")
SNOOPY_BOT_TOKEN = os.getenv("ENV_VAR_SNOOPY_BOT_TOKEN")
SNOOPY_BOT_ADMIN = os.getenv("ENV_VAR_SNOOPY_ADMIN")

# MEXC
MEXC_API_ACCESS_KEY = os.getenv("ENV_VAR_MEXC_API_ACCESS_KEY")
MEXC_API_SECRET_KEY = os.getenv("ENV_VAR_MEXC_API_SECRET_KEY")
