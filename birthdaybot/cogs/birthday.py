import discord
import datetime

from discord import app_commands
from ..models import Guild, Birthday
from ..bot import client              

# admin command   
# make the command only visible to admin (or restrict to certain roles): 
# Server Settings > Integrations > Birthday Bot > /add-birthday-user > Add Roles or Members > @everyone > X
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
    await interaction.response.defer(thinking=True, ephemeral=True)
    if interaction.user.guild_permissions.administrator:
        await add_user_birthday_func(interaction, day, month, user)


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
    await interaction.response.defer(thinking=True, ephemeral=True)
    await add_user_birthday_func(interaction, day, month, interaction.user)
    

async def add_user_birthday_func(interaction: discord.Interaction, day:int, month:int, user: discord.User):
    guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
    if guild.channel_id is None:
        await interaction.edit_original_response(
        content=f"Please contact a moderator to first set a channel with the `/set_channel` command."
    )
        return
    
    if (db_entry := Birthday.get_or_none((Birthday.guild_id == interaction.guild.id) & (Birthday.user_id == user.id))) is not None:
        db_entry: Birthday
        await interaction.edit_original_response(
        content=f"This user's brithday previously already had been added. It is set to **{db_entry.date.strftime('%B')} {db_entry.date.strftime('%d')}**. If you would like to change it, please delete this entry first and add a new one."
    )
        return

    user_birthday = Birthday.create(guild_id=interaction.guild.id, user_id=user.id, date=datetime.date(month=month, day=day, year=1970))
    
    await interaction.edit_original_response(
        content=f"Your birthday was successfully added as **{user_birthday.date.strftime('%B')} {user_birthday.date.strftime('%d')}**! 🥳🎂"
    )

@client.tree.command(name="remove-birthday", description="Remove your birthday from the list")
async def remove_birthday(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if (db_entry := Birthday.get_or_none((Birthday.guild_id == interaction.guild.id) & (Birthday.user_id == interaction.user.id))) is not None:
        db_entry: Birthday
        db_entry.delete_instance()
        await interaction.edit_original_response(
            content=f"Your birthday has been removed from the list. 💥"
        )
    else:
        await interaction.edit_original_response(
            content=f"Your birthday had not been tracked so far."
        )

# admin command
@client.tree.command(name="remove-birthday-user", description="Remove your birthday from the list")
@app_commands.describe(
    user="Who's birthday do you want to remove?"
)
async def remove_birthday_user(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if interaction.user.guild_permissions.administrator:
        if (db_entry := Birthday.get_or_none((Birthday.guild_id == interaction.guild.id) & (Birthday.user_id == user.id))) is not None:
            db_entry: Birthday
            db_entry.delete_instance()
            await interaction.edit_original_response(
                content=f"{user.display_name}'s birthday has been removed from the list. 💥"
            )
        else:
            await interaction.edit_original_response(
                content=f"{user.display_name}'s birthday had not been tracked so far."
            )

@client.tree.command(name="get-birthday", description="Returns the birthday you added (only you can see the response)")
async def get_birthday(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if (db_entry := Birthday.get_or_none((Birthday.guild_id == interaction.guild.id) & (Birthday.user_id == interaction.user.id))) is not None:
        db_entry: Birthday
        await interaction.edit_original_response(
            content=f"Your birthday is set as **{db_entry.date.strftime('%B')} {db_entry.date.strftime('%d')}**! 🎈🍰"
            f"\n \n I hope that is correct? 🤔 \n To change it, please delete the current entry with `/remove-birthday` and add it again with `/add-birthday`.")
    else:
        await interaction.edit_original_response(
            content=f"Your birthday is not yet being tracked. Add it with the `/add-birthday` command. ✨")

# admin command  
@client.tree.command(name="get-birthdays", description="Returns all tracked birthdays for this server.")
async def get_birthdays(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    birthday_string = ""
    if interaction.user.guild_permissions.administrator:
        for db_entry in Birthday.select().where(Birthday.guild_id == interaction.guild.id).order_by(Birthday.date):
            db_entry: Birthday
            birthday_string = birthday_string + f"**{db_entry.date.strftime('%B')} {db_entry.date.strftime('%d')} -  <@{db_entry.user_id}>** 🎈 \n"
        await interaction.edit_original_response(content=birthday_string, allowed_mentions=discord.AllowedMentions(users=False))

# admin command  
@client.tree.command(name="upcoming-birthdays", description="Returns the three next upcoming birthdays.")
async def upcoming_birthdays(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    birthday_string = "The next upcoming birthdays are: \n\n"
    if interaction.user.guild_permissions.administrator:
        today = datetime.datetime.now()
        next_occurrence_list = []
        for db_entry in Birthday.select().where((Birthday.guild_id == interaction.guild.id)).order_by(Birthday.date):
            db_entry: Birthday
           
            temp = db_entry
            temp.date = temp.date.replace(year=today.year)
          
            has_passed = temp.date < today.date()
            if has_passed:
                temp.date = temp.date.replace(year=(today.year + 1))
            next_occurrence_list.append(temp)

        next_occurrence_list.sort(key=lambda element: element.date)
        for index in range(3):
            next = next_occurrence_list[index]
            days_until = abs((next.date - today.date()).days)
            birthday_string = birthday_string + f"- <@{next.user_id}> - {next.date.strftime('%A')}, {next.date.strftime('%B')} {next.date.strftime('%d')} {next.date.strftime('%Y')} 🎂 in **{days_until}** days.\n"
        await interaction.edit_original_response(content=birthday_string, allowed_mentions=discord.AllowedMentions(users=False))
       