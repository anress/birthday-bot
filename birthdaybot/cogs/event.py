import discord
import logging
import datetime

from discord import app_commands
from ..models import Guild, Event
from ..bot import client
    
@client.tree.command(name="add-event", description="Add a custom event")
@app_commands.describe(
    day="Day the event takes place.",
    month="Month the event takes place.",
    year="Year of the event. If not set, it will automatically take the next occurrence of the date.",
    description="Tell us about this event.",
    repeat_annually="Set whether this is a yearly reccurring event."
)
async def add_event(
    interaction: discord.Interaction,
    day: app_commands.Range[int, 1, 31],
    month: app_commands.Range[int, 1, 12],
    year: int,
    description: str,
    repeat_annually: bool
):
    await interaction.response.defer(thinking=True)
    print(interaction.user.roles)
    guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
    if guild.channel_id is None:
        await interaction.edit_original_response(
        content=f"You first must set a channel with the `/set_channel` command."
    )
    result = day + month
    user_birthday = Event.create(interaction.guild.id, interaction.user.id, datetime.date(month=month, day=day, year=year), description=description, repeatAnnually=repeat_annually)
    
    interaction.guild.get_channel(guild.channel_id).send(user_birthday)
    await interaction.edit_original_response(
        content=f"The result is {result}."
    )
