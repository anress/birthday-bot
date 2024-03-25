import datetime
import discord
from typing import List
from discord.ext import tasks
import random
import logging
from ..models import Guild, Birthday, Event
from birthdaybot.constants import SCHEDULER_TIME, BIRTHDAY_QUOTES, BIRTHDAY_IMAGES, EMBED_COLORS

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
clean_up_time = datetime.time(hour=23, minute=59, tzinfo=utc)

class Scheduler:
    def __init__(self, client):
        logging.info(f"Loading scheduled tasks.")
        self.client = client
        self.check_birthdays_events.start()
        self.check_periodically.start()
        self.clean_up.start()

    def cog_unload(self):
        logging.info(f"Unloading scheduled tasks")
        self.check_birthdays_events.cancel()
        self.check_periodically.cancel()
        self.clean_up.cancel()

    ## do midnight clean up loop
    @tasks.loop(minutes=30)
    async def check_periodically(self):
        logging.info(f"Birthday bot is still up and running!")

    ## do midnight clean up loop
    @tasks.loop(time=clean_up_time)
    async def clean_up(self):
        logging.info(f"Starting clean up")
        client_guilds = [guild async for guild in self.client.fetch_guilds(limit=None)]
        for guild in client_guilds:
            guild: discord.Guild
            if (db_entry_guild := Guild.get_or_none((Guild.guild_id == guild.id) & (Guild.birthday_role_id is not None))) is not None:
                db_entry_guild: Guild

                guild_members = [member async for member in guild.fetch_members(limit=None)]
                for member in guild_members:
                    member: discord.Member
                    
                    guild_roles: List[discord.Role] = await guild.fetch_roles()
                    role = next((x for x in guild_roles if x.id == db_entry_guild.birthday_role_id), None)
              
                    if role is not None:
                        await member.remove_roles(role)

        logging.info(f"Clean up completed.")

    @tasks.loop(time=SCHEDULER_TIME)
    async def check_birthdays_events(self):        
        logging.info(f"Checking for birthdays + events")
        today = datetime.datetime.now()

        for db_entry in Birthday.select().where((Birthday.date.day == today.day) & (Birthday.date.month == today.month)):
            db_entry: Birthday
            
            if (db_entry_guild := Guild.get_or_none(Guild.guild_id == db_entry.guild_id)) is not None:
                db_entry_guild: Guild
                if db_entry_guild.channel_id is not None:
                    guild: discord.Guild = await self.client.fetch_guild(db_entry_guild.guild_id)
                    channel: discord.TextChannel = await guild.fetch_channel(db_entry_guild.channel_id)
                  
                    member = await guild.fetch_member(db_entry.user_id)

                    
                    logging.info(f"Today's birthday: {member.display_name} on guild {guild.name}")

                    guild_roles: List[discord.Role] = await guild.fetch_roles()
                    role = next((x for x in guild_roles if x.id == db_entry_guild.birthday_role_id), None)
              
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
                  
                  
                    logging.info(f"Today's event: {db_entry.title} on guild {guild.name}")

                    embed: discord.Embed = discord.Embed(title=db_entry.title, description=db_entry.description, color=random.choice(EMBED_COLORS))
                    if db_entry.image_url is not None:
                        embed.set_image(url=db_entry.image_url)
                    embed.set_footer(text="Powered by anjress", icon_url="https://anja.codes/logo192.png")
                    await channel.send(embed=embed)
        
        logging.info(f"Finished checking for birthdays + events")