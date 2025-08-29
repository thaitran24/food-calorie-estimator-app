import pytz
from datetime import datetime

def now():
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    return datetime.now(bangkok_tz)