"""Simple test file illustrating how to write database migrations.

Run via `python migrations/test_add_and_remove_columns.py`.

Make sure to make the corresponding changes in the respective `models.py` file.
"""
import peewee as pw

from playhouse.migrate import SqliteMigrator, migrate
from birthdaybot.models import BOT_DB

migrator = SqliteMigrator(BOT_DB)

# ## remove column again
# migrate(
#     migrator.drop_index('birthday', 'birthday_guild_id')
# )
# migrate(
#     migrator.drop_column('birthday', 'guild_id')
# )


## add a new column belonging to a TextField to the guild table
guildId = pw.IntegerField(default=0)
userId = pw.IntegerField(default=0, unique=True)



# migrate(
#     migrator.add_column('event', 'user_id', guildId)
# )


# migrate(
#     migrator.add_column('birthday', 'user_id', userId)
# )



