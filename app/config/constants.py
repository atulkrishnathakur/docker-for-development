import os

from dotenv import load_dotenv
load_dotenv()

class Constants:
    ON: bool = True
    OFF: bool = False
    STATUS_UNAUTHORIZED=False
    STATUS_FORBIDDEN=False
    STATUS_BAD_REQUEST=False
    STATUS_OK=True
    DB_ACTIVE_STATUS = 1
    DB_INACTIVE_STATUS = 0

constants = Constants()