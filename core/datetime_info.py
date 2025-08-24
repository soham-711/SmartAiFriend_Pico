from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    now = datetime.now()
    return now.strftime("%d-%m-%Y")

def get_day():
    now = datetime.now()
    return now.strftime("%A")
