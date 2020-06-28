import os
from datetime import datetime
from uuid import uuid4


def create_unique_filename(filename):
    filename, extension = os.path.splitext(filename)
    current_datetime = datetime.now()
    timestamp = current_datetime.timestamp()
    return f'{uuid4().hex}_{timestamp}{extension}'
