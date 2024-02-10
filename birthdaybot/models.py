import peewee as pw

from birthdaybot import BOT_DB

class Guild(pw.Model):
    guild_id = pw.IntegerField(null=False, unique=True)
    channel_id = pw.IntegerField(null=True)

    def __repr__(self) -> str:
        return f"<Guild: {self.get_id()}, guild_id={self.guild_id}>"

    class Meta:
        database = BOT_DB



BOT_DB.create_tables([Guild])