import datetime
import discord
import math
from birthdaybot.constants import MESSAGE_MAX_LEN

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