import discord
import logging
import datetime

from discord import app_commands, ui
from ..models import Guild, Event
from ..bot import client

class EventModal(ui.Modal, title='Create new event'):
    description = ui.TextInput(label='Description of your event', style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        global temp
        temp = self.description
        self.on_submit_interaction = interaction
        self.stop()

        return self.description

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
    modal = EventModal()
   
    await interaction.response.send_modal(modal)

    response = await modal.wait() # Wait for the modal to respond
    print(response)
    print(modal.description)
    # Edit the message

    # Send the confirmation
    await modal.on_submit_interaction.response.send_message(f"The message was edited successfully :slight_smile:", ephemeral=True)
   
    Event.create(guild_id=interaction.guild.id, user_id= interaction.user.id, date=datetime.date(month=month, day=day, year=year), description=modal.description, repeat_annually=repeat_annually)
    
    # guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
    # if guild.channel_id is None:
    #     await interaction.edit_original_response(
    #     content=f"You first must set a channel with the `/set_channel` command."
    # )
    
