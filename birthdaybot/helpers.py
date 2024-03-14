import datetime
import calendar
import discord
import math
import re
from birthdaybot.constants import MESSAGE_MAX_LEN

## check if date is out of range for month and leap year, in case of year attirbute given
def is_legitmate_date(day:int, month:int, year:int, check_year:bool = False):
    if month == 2:
        if day > 29:
            return False
        if (day == 29) & check_year & (calendar.isleap(year) is False):
            return False
    if (month in [4, 6, 9, 11]) & (day > 30):
        return False
    
    return True


def date_formatter(date: datetime):
   return f"{date.strftime('%A')}, {date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}"

async def send_long_message(message: str, interaction: discord.Interaction, already_responded: bool = False):
    if len(message) > MESSAGE_MAX_LEN:
        start_index = 0
        max_iterations =  (math.ceil(len(message) / MESSAGE_MAX_LEN))
        
        if not already_responded:
            await interaction.edit_original_response(content=message[0:MESSAGE_MAX_LEN])
            start_index = 1
        for part in range(start_index, max_iterations):      
            string_part = message[MESSAGE_MAX_LEN * part:min(MESSAGE_MAX_LEN * (part +1), len(message))]
            if part is not 0:
                string_part = "..." + string_part
            if part is not max_iterations-1:
                string_part = string_part + "..."
            await interaction.followup.send(content=string_part, ephemeral=True)
    else:
        if not already_responded:
            await interaction.edit_original_response(content=message)
        else:
            await interaction.followup.send(content=message, ephemeral=True)

def is_valid_url(url: str):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

def is_valid_date(date: str):
    # dd/MM/yyyy
    regex = re.compile(
        r"(^(((0[1-9]|1[0-9]|2[0-8])[\/](0[1-9]|1[012]))|((29|30|31)[\/](0[13578]|1[02]))|((29|30)[\/](0[4,6,9]|11)))[\/](19|[2-9][0-9])\d\d$)|(^29[\/]02[\/](19|[2-9][0-9])"
        r"(00|04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)$)"
    )    
    return date is not None and regex.search(date)