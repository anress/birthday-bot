import discord
import logging

from discord import app_commands

from ..bot import client

@client.tree.command(name="add-me", description="Add two numbers.")
@app_commands.describe(
    number1="The first number.",
    number2="The second number."
)
async def add_numbers(
    interaction: discord.Interaction,
    number1: int,
    number2: int,
):
    await interaction.response.defer(thinking=True)
    result = number1 + number2
    await interaction.edit_original_response(
        content=f"The result is {result}."
    )
