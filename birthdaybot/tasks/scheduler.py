import datetime
import discord
from discord.ext import commands, tasks
import random
from ..models import Guild, Birthday 
from birthdaybot.constants import BIRTHDAY_QUOTES, BIRTHDAY_IMAGES, EMBED_COLORS

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
time = datetime.time(hour=8, minute=30, tzinfo=utc)

class Scheduler:
    def __init__(self, client):
        self.client = client
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    @tasks.loop(seconds=50)
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
                    embed: discord.Embed = discord.Embed(description=f"## ᨏᨐᨓ **Happy Birthday {member.display_name}!** ᨓᨐᨏ \n### ❀⊱┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄⊰❀\n\n"
                                                         f"{random.choice(BIRTHDAY_QUOTES)}\n\n" 
                                                         f"₊˚✧꒰ Everyone wish **<@{member.id}>** a happy birthday! ꒱₊˚✧\n", color=random.choice(EMBED_COLORS))
                    embed.set_image(url=random.choice(BIRTHDAY_IMAGES))
                    embed.set_footer(text="Powered by anjress", icon_url="https://anja.codes/logo192.png")
                    await channel.send(embed=embed)