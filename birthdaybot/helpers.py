import datetime

def date_formatter(date: datetime):
   return f"{date.strftime('%A')}, {date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}"