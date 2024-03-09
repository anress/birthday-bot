import discord
import logging
import datetime
import math
import random

from discord import app_commands, ui
from ..models import Guild, Event
from ..bot import client
from birthdaybot.constants import EMBED_COLORS, MESSAGE_MAX_LEN
from birthdaybot.helpers import date_formatter

class EventModal(ui.Modal, title='Create new event'):
    event_title = ui.TextInput(label='Event title')
    description = ui.TextInput(label='Description of your event', style=discord.TextStyle.paragraph)
    image_url = ui.TextInput(label='Add an image (optional)', required=False)
    async def on_submit(self, interaction: discord.Interaction):
        self.on_submit_interaction = interaction
        self.stop()


@client.tree.command(name="add-event", description="Add a custom event")
@app_commands.describe(
    day="Day the event takes place.",
    month="Month the event takes place.",
    year="Year of the event. If not set, it will automatically take the next occurrence of the date.",
    repeat_annually="Set whether this is a yearly reccurring event."
)
async def add_event(
    interaction: discord.Interaction,
    day: app_commands.Range[int, 1, 31],
    month: app_commands.Range[int, 1, 12],
    year: int,
    repeat_annually: bool
):
    # await interaction.response.defer(thinking=True)
    guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
    if guild.channel_id is None:
        await interaction.edit_original_response(
        content=f"Please contact a moderator to first set a channel with the `/set_channel` command."
    )
        return
    
    modal = EventModal()
   
    await interaction.response.send_modal(modal)

    response = await modal.wait() # Wait for the modal to respond

    # Send the confirmation   
    event = Event.create(guild_id=interaction.guild.id, user_id= interaction.user.id, date=datetime.date(month=month, day=day, year=year), repeat_annually=repeat_annually, title=modal.event_title, description=modal.description, image_url=modal.image_url)
    
    await modal.on_submit_interaction.response.send_message(f"Successfully added your event! 💃 \nThe ID of your event is: `{event.id}`, in case you want to preview or edit it later.", ephemeral=True)

   
@client.tree.command(name="my-events", description="Returns all events you ever added.")
async def my_events(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    events_string = ""
    for db_entry in Event.select().where((Event.guild_id == interaction.guild.id) and (Event.user_id == interaction.user.id)).order_by(Event.date):
        db_entry: Event
        
        today = datetime.datetime.now()
        next_occurence_date = db_entry.date.replace(year=today.year)
        has_passed = db_entry.date < today.date()
        if has_passed:
            next_occurence_date = next_occurence_date.replace(year=(today.year + 1))

        repeat_annually_str = (f'Yes ✅ *(Next occurence: {date_formatter(next_occurence_date)})*' if db_entry.repeat_annually   else 'No :x:')
        image_url_str = (db_entry.image_url if db_entry.image_url is not None else "-")

        events_string = (f"{events_string} **ID:** `{db_entry.id}` \n**Title:** {db_entry.title}\n**Description:** {db_entry.description}\n"
        f"**Date:** {date_formatter(db_entry.date)}\n**Repeated annually:** {repeat_annually_str}\n"
        f"**Image URL:**  {image_url_str}"
        f"\n\n --- \n\n")

    if len(events_string) > MESSAGE_MAX_LEN:
        await interaction.edit_original_response(content=events_string[0:MESSAGE_MAX_LEN])
        for part in range(1, (math.ceil(len(events_string) / MESSAGE_MAX_LEN))):      
            string_part = events_string[MESSAGE_MAX_LEN * part:min(MESSAGE_MAX_LEN * (part +1), len(events_string))]
            await interaction.followup.send(content=string_part, ephemeral=True)
    else:
        await interaction.edit_original_response(content=events_string)
    


@client.tree.command(name="preview-event", description="Preview one of your events.")
@app_commands.describe(
   event_id="ID of your event that you want to preview"
)
async def preview_event(
    interaction: discord.Interaction,
    event_id: int
    ):
    await interaction.response.defer(thinking=True, ephemeral=True)
  
    if (db_entry := Event.get_or_none((Event.guild_id == interaction.guild.id) & (Event.user_id == interaction.user.id) & (Event.id == event_id))) is not None:
        db_entry: Event
        embed: discord.Embed = discord.Embed(title=db_entry.title, description=db_entry.description, color=random.choice(EMBED_COLORS))
        if db_entry.image_url is not None:
            embed.set_image(url=db_entry.image_url)
        embed.set_footer(text="Powered by anjress", icon_url="https://anja.codes/logo192.png")
        await interaction.edit_original_response(embed=embed)
    else:
        await interaction.edit_original_response(content=f"We couldn't find an event of yours by the ID of `{event_id}`. ☹️ \nCheck with the command `/my-events` the IDs of all your events.")


@client.tree.command(name="delete-event", description="Delete one of your events.")
@app_commands.describe(
    event_id="ID of your event that you want to delete."
)
async def remove_birthday_user(interaction: discord.Interaction, event_id: int):
    await interaction.response.defer(thinking=True, ephemeral=True)

    if (db_entry := Event.get_or_none((Event.guild_id == interaction.guild.id) & (Event.user_id == interaction.user.id) & (Event.id == event_id))) is not None:
        db_entry: Event
        event_title = db_entry.title
        db_entry.delete_instance()
        await interaction.edit_original_response(
            content=f"The event {event_title} with the ID {event_id} has been deleted. 💥"
        )
    else:
        await interaction.edit_original_response(content=f"We couldn't find an event of yours by the ID of `{event_id}`. ☹️ \nCheck with the command `/my-events` the IDs of all your events.")
    
  
    
