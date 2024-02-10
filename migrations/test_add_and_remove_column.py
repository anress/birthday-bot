"""Simple test file illustrating how to write database migrations.

Run via `python migrations/test_add_and_remove_columns.py`.

Make sure to make the corresponding changes in the respective `models.py` file.
"""
import peewee as pw

from playhouse.migrate import SqliteMigrator, migrate
from birthdaybot import BOT_DB

migrator = SqliteMigrator(BOT_DB)


## add a new column belonging to a TextField to the guild table
comment_field = pw.TextField(default='')
migrate(
    migrator.add_column('guild', 'comment', comment_field)
)


## remove column again
migrate(
    migrator.drop_column('guild', 'comment')
)