from datetime import datetime

def get_utcnow():
    return datetime.utcnow()

def getNow():
    utc_now = get_utcnow()
    epoch = datetime(1970,1,1,0,0)
    delta = round((utc_now - epoch).total_seconds() * 1000.0)
    return delta