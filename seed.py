"""Utility file to seed ufo_reports database from NUFORC data in seed_data/"""

import datetime
from sqlalchemy import func

from model import Event, connect_to_db, db
from server import app

def load_events():
    """Load events from seed_data files into database"""

    