import discord
import logging

from discord.ext import commands
from pathlib import Path
import traceback

from .models import Guild


discord.utils.setup_logging()
intents = discord.Intents.default()
# intents.members = True
intents.message_content = True
# intents.guilds = True

ADMIN_GUILDS = [discord.Object(id=guild.guild_id) for guild in Guild.select() if guild.is_admin_guild]

class DiscordBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        for admin_guild in ADMIN_GUILDS:
            self.tree.copy_global_to(guild=admin_guild)
            await self.tree.sync(guild=admin_guild)

client = DiscordBotClient(intents=intents)

@client.event
async def on_guild_join(guild: discord.Guild):
    logging.info(f"Joined {guild}.")
    Guild.create(guild_id=guild.id)
    await client.tree.sync(guild=discord.Object(id=guild.id))


@client.tree.command(name="hello", description="this is a short description")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message("this command has been triggered YEP")


@client.tree.command(
    name="set_channel",
    description="Set the current channel as default channel for the bot to post updates in.",
)
async def set_channel(interaction: discord.Interaction):
    try:
            await interaction.response.defer(thinking=True, ephemeral=True)
            guild = Guild.get(Guild.guild_id == interaction.guild.id)
            guild.channel_id = interaction.channel_id
            guild.save()
            channelName = interaction.channel.name
            await interaction.edit_original_response(
                content=f"Set the default channel to `{channelName}`!"
            )
    except:
            await interaction.edit_original_response(
                content="An error occurred while trying to set the default channel."
            )
            logging.error(f"Could not set the default channel.")
            traceback.print_exc()


@client.tree.command(
    name="sync",
    description="Synchronizes the global command tree of the client",
    guilds=ADMIN_GUILDS,
)
async def command_sync(interaction: discord.Interaction):
    await client.tree.sync()
    await interaction.response.send_message("Global commands syncronized successfully.", ephemeral=True)


@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user.name}")
    for guild in client.guilds:
            if not (Guild.get(Guild.guild_id == guild.id)):
                Guild.create(guild_id=guild.id)
                await client.tree.sync(guild=discord.Object(id=guild.id))