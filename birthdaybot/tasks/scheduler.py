import datetime
import discord
from typing import List
from discord.ext import commands, tasks
import random
from ..models import Guild, Birthday, Event
from birthdaybot.constants import BIRTHDAY_QUOTES, BIRTHDAY_IMAGES, EMBED_COLORS

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
time = datetime.time(hour=21, minute=59, tzinfo=utc)


clean_up_time = datetime.time(hour=0, minute=0, tzinfo=utc)

class Scheduler:
    def __init__(self, client):
        self.client = client
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    ## do midnight clean up loop
    @tasks.loop(time=time)
    async def my_task(self):

    @tasks.loop(time=time)
    async def my_task(self):
        today = datetime.datetime.now()
        print("My task is running!")

        for db_entry in Birthday.select().where((Birthday.date.day == today.day) & (Birthday.date.month == today.month)):
            db_entry: Birthday
            
            if (db_entry_guild := Guild.get_or_none(Guild.guild_id == db_entry.guild_id)) is not None:
                db_entry_guild: Guild
                if db_entry_guild.channel_id is not None:
                    guild: discord.Guild = await self.client.fetch_guild(db_entry_guild.guild_id)
                    channel: discord.TextChannel = await guild.fetch_channel(db_entry_guild.channel_id)
                  
                    member = await guild.fetch_member(db_entry.user_id)
                    roles: List[discord.Role] = await guild.fetch_roles()
                    print(guild.roles)
                    print(db_entry_guild.birthday_role_id)
                    print(roles)
                    role = next((x for x in roles if x.id == db_entry_guild.birthday_role_id), None)
                    print(role)
                    if role is not None:
                        await member.add_roles(role)
                    
                    embed: discord.Embed = discord.Embed(description=f"## ᨏᨐᨓ **Happy Birthday {member.display_name}!** ᨓᨐᨏ \n### ❀⊱┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄⊰❀\n\n"
                                                         f"{random.choice(BIRTHDAY_QUOTES)}\n\n" 
                                                         f"₊˚✧꒰ Everyone wish **<@{member.id}>** a happy birthday! ꒱₊˚✧\n", color=random.choice(EMBED_COLORS))
                    embed.set_image(url=random.choice(BIRTHDAY_IMAGES))
                    embed.set_footer(text="Powered by anjress", icon_url="https://anja.codes/logo192.png")
                    await channel.send(embed=embed)

        for db_entry in Event.select().where(((Event.date.day == today.day) & (Event.date.month == today.month) & (Event.date.year == today.year)) | ((Event.date.day == today.day) & (Event.date.month == today.month) & (Event.repeat_annually))):
            db_entry: Event
            
            if (db_entry_guild := Guild.get_or_none(Guild.guild_id == db_entry.guild_id)) is not None:
                db_entry_guild: Guild
                if db_entry_guild.channel_id is not None:
                    guild: discord.Guild = await self.client.fetch_guild(db_entry_guild.guild_id)
                    channel: discord.TextChannel = await guild.fetch_channel(db_entry_guild.channel_id)
                  
                    embed: discord.Embed = discord.Embed(title=db_entry.title, description=db_entry.description, color=random.choice(EMBED_COLORS))
                    if db_entry.image_url is not None:
                        embed.set_image(url=db_entry.image_url)
                    embed.set_footer(text="Powered by anjress", icon_url="https://anja.codes/logo192.png")
                    await channel.send(embed=embed)