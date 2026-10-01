"""
Proxy serasi ke belakang (backward-compatible) untuk db_models.py.
Memastikan sebarang kod atau skrip lama yang import db_utils terus berfungsi tanpa ralat.
"""

from models.db_models import (
    get_connection,
    check_connection,
    get_recommendations,
    get_lipstick_recommendations,
    SKINTONE_ORDER
)
from config import get_db_config

DB_CONFIG = get_db_config()