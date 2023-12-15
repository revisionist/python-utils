import logging
import time

logger = logging.getLogger(__name__)


def get_current_time_ms():

    return int(time.time() * 1000)

