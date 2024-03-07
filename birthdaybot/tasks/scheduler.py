import datetime
import discord
from discord.ext import commands, tasks
from ..models import Guild, Birthday 

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

    @tasks.loop(seconds=30)
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
                    await channel.send(f"# ✨✨🎈🎂🥳🍰 HAPPY BIRTHDAY <@{member.id}>!!! 🥳🍰🎈✨✨🎂🎈🥳🥳")