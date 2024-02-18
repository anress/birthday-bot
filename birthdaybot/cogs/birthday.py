import discord
import logging
import datetime

from discord import app_commands
from discord.ext.commands import has_permissions
from ..models import Guild, Birthday
from ..bot import client


@has_permissions(administrator=True)
@client.tree.command(name="add-birthday-user", description="Add a specific user's birthday")
@app_commands.describe(
    day="Day you were born on.",
    month="Month you were born in.",
    user="Who's birthday is ist?"
)
async def add_birthday_user (
    interaction: discord.Interaction,
    day: app_commands.Range[int, 1, 31],
    month: app_commands.Range[int, 1, 12],
    user: discord.User
):
    await interaction.response.defer(thinking=True)
    if interaction.user.guild_permissions.administrator:
        await interaction.edit_original_response(
            content=f"You are an admin! Wonderful!"
        )
    else:
        await interaction.edit_original_response(
            content=f"You are not an admin. Pleb."
        )
    # await add_user_birthday_func(interaction, day, month, user)


@has_permissions(administrator=True)
@client.tree.command(name="add-birthday", description="Add your birthday")
@app_commands.describe(
    day="Day you were born on.",
    month="Month you were born in."
)
async def add_birthday(
    interaction: discord.Interaction,
    day: app_commands.Range[int, 1, 31],
    month: app_commands.Range[int, 1, 12]
):
    await interaction.response.defer(thinking=True)
    await add_user_birthday_func(interaction, day, month, interaction.user)
    

async def add_user_birthday_func(interaction: discord.Interaction, day:int, month:int, user: discord.User):
    guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
    if guild.channel_id is None:
        await interaction.edit_original_response(
        content=f"You first must set a channel with the `/set_channel` command."
    )
        return
    
    if (db_entry := Birthday.get_or_none(Birthday.guild_id == interaction.guild.id and Birthday.user_id == user.id)) is not None:
        db_entry: Birthday
        await interaction.edit_original_response(
        content=f"This user's brithday previously already had been added. It is set to {db_entry.date}. If you would like to change it, please delete this entry first and add a new one."
    )
        return

    result = day + month
    user_birthday = Birthday.create(interaction.guild.id, interaction.user.id, datetime.date(month=month, day=day))
    
    interaction.guild.get_channel(guild.channel_id).send(user_birthday)
    await interaction.edit_original_response(
        content=f"The result is {result}."
    )

@client.tree.command(name="remove-birthday", description="Remove your birthday from the list")
async def remove_birthday(interaction: discord.Interaction):
    if (db_entry := Birthday.get_or_none(Birthday.guild_id == interaction.guild.id and Birthday.user_id == interaction.user.id)) is not None:
        db_entry: Birthday
        db_entry.delete()
        await interaction.edit_original_response(
            content=f"Your birthday has been removed from the list."
        )
    else:
        await interaction.edit_original_response(
            content=f"Your birthday had not been tracked so far."
        )