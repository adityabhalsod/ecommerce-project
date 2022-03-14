# settings.py
from __future__ import absolute_import, unicode_literals

import logging

from dotenv import load_dotenv

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only

env_path = Path(".") / Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


logger = logging.getLogger(__name__)


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ["celery_app"]
