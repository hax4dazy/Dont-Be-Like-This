from peewee import *
import os

os.makedirs("db", exist_ok=True)
db = SqliteDatabase("db/database.db", pragmas={"foreign_keys": 1})


class MySQLModel(Model):
    class Meta:
        database = db

class GuildSettings(MySQLModel):
    ServerID = BigIntegerField(primary_key=True)
    ChannelID = BigIntegerField()
    WebHookURL = CharField(null=True)

class BotSettings(MySQLModel):
    BotToken = CharField()


if __name__ == "__main__":
  db.create_tables([GuildSettings, BotSettings], safe=True)