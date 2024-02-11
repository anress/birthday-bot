import peewee as pw

from pathlib import Path

# database is created in parent directory of this file
BOT_DB = pw.SqliteDatabase(Path(__file__).parent.parent / 'discordbot.db')

class Guild(pw.Model):
    guild_id = pw.IntegerField(null=False, unique=True)
    channel_id = pw.IntegerField(null=True)
    is_admin_guild = pw.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<Guild: {self.get_id()}, guild_id={self.guild_id}>"

    class Meta:
        database = BOT_DB

BOT_DB.create_tables([Guild])