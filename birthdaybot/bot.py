import discord
import logging

from discord import app_commands
from discord.ext.commands import has_permissions

from .models import Guild, Birthday, Event

from .tasks.scheduler import Scheduler


discord.utils.setup_logging()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

ADMIN_GUILDS = [
    discord.Object(id=guild.guild_id) for guild in Guild.select()
    if guild.is_admin_guild
]

class BirthdayBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    # async def on_disconnect(self):
        # for task in self.task_containers:
          #  task.cog_unload()

    async def setup_hook(self):
        logging.info(f"Logged in as {self.user.name}")

        client_guilds = [guild async for guild in self.fetch_guilds(limit=None)]
        for guild in client_guilds:
            if Guild.get_or_none(Guild.guild_id == guild.id) is None:
                Guild.create(guild_id=guild.id)

        client_guild_ids = [guild.id for guild in client_guilds]
        for guild in Guild.select():
            guild: Guild
            if not guild.guild_id in client_guild_ids:
                guild.delete_instance()
        logging.info(f"Finished database cleanup.")
             
        for admin_guild in ADMIN_GUILDS:
            self.tree.copy_global_to(guild=admin_guild)
            await self.tree.sync(guild=admin_guild)
            logging.info(f"Synchronized command tree with commands {[cmd.name for cmd in self.tree.get_commands(guild=admin_guild)]} to admin servers.")

        self.task_containers = [
            Scheduler(self),
        ]

client = BirthdayBotClient(intents=intents)

@client.event
async def on_guild_join(guild: discord.Guild):
    logging.info(f"Joined {guild}.")
    Guild.create(guild_id=guild.id)

@client.event
async def on_guild_remove(guild: discord.Guild):
     logging.info(f"Left / got removed from {guild}.")
     if (db_entry := Guild.get_or_none(Guild.guild_id == guild.id)) is not None:
        db_entry.delete_instance()
        # and delete all events + birthdays from guild
        Birthday.delete().where(Birthday.guild_id == guild.id).execute()
        Event.delete().where(Event.guild_id == guild.id).execute()

if ADMIN_GUILDS:
    @client.tree.command(
        name="sync",
        description="Synchronizes the global command tree of the client",
        guilds=ADMIN_GUILDS,
    )
    async def sync_command_tree(interaction: discord.Interaction):
        await client.tree.sync()
        logging.info(f"Synchronized command tree with global commands {[cmd.name for cmd in client.tree.get_commands()]}.")
        await interaction.response.send_message("Global commands syncronized successfully.", ephemeral=True)

@has_permissions(administrator=True)
@client.tree.command(
    name="set-channel",
    description="Set the default channel for the bot to post updates in.",
)
@app_commands.describe(
     channel="A text channel."
)
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if (db_entry := Guild.get_or_none(Guild.guild_id == channel.guild.id)) is not None:
        db_entry: Guild
        db_entry.channel_id = channel.id
        db_entry.save()
    else:
        Guild.create(guild_id=channel.guild.id, channel_id=channel.id)
    await interaction.edit_original_response(
        content=f"Set the default channel to <#{channel.id}>!"
    )
