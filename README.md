# Discord bot template

This is a generic template for creating a discord bots with slash commands.

## Packages

- written with [discord.py](discordpy.readthedocs.io) and [poetry](https://python-poetry.org/docs/basic-usage/)
- used ORM: [peewee](https://docs.peewee-orm.com/)
- databse: [SQLite](https://www.sqlite.org/)

## Multi server support

The bot will write any new discord servers it joins into the database. Set `is_admin_guild` to `true` to use a specific server as development server. 
This server will be able to execute the `sync` command to synchronize the global command tree of the client.

## How to

1. Start poetry shell: `poetry shell`
2. Install dependencies: `poetry install`
3. Start the bot: `python -m discordbottemplate`

