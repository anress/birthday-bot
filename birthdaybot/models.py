import peewee as pw

from pathlib import Path

# database is created in parent directory of this file
BOT_DB = pw.SqliteDatabase(Path(__file__).parent.parent / 'birthdaybot.db')

class Guild(pw.Model):
    guild_id = pw.IntegerField(null=False, unique=True)
    channel_id = pw.IntegerField(null=True)
    is_admin_guild = pw.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<Guild: {self.get_id()}, guild_id={self.guild_id}>"

    class Meta:
        database = BOT_DB

class Birthday(pw.Model):
    guild_id = pw.IntegerField(null=False, unique=True)
    user_id = pw.IntegerField(null=False)
    date = pw.DateField(null=False)

    def __repr__(self) -> str:
        return f"<Birthday: {self.get_id()}, guild_id={self.guild_id}, user_id={self.user_id}, date={self.date}>"

    class Meta:
        database = BOT_DB

class Event(pw.Model):
    guild_id = pw.IntegerField(null=False, unique=True)
    user_id = pw.IntegerField(null=False)
    date = pw.DateField(null=False)
    description = pw.TextField(null=False)
    repeatAnnually = pw.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<Event: {self.get_id()}, guild_id={self.guild_id}, user_id={self.user_id}, date={self.date}, description={self.description} repeatAnnually={self.repeatAnnually}>"

    class Meta:
        database = BOT_DB        

BOT_DB.create_tables([Guild, Birthday, Event])


