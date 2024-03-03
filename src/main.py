import discord, aiohttp
from os import environ
from db import *

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

try:
    discord_token = BotSettings.get(BotSettings.id == 1).BotToken
except Exception as e:
    print(f'Token not found, taking env variable BOT_TOKEN and using that as the token.\nPlease remove the env variable and restart the bot')
    with db.atomic() as txn:    
        BotSettings.create(BotToken=environ.get("BOT_TOKEN"))
    exit()

class YesOrNoButtons(discord.ui.View):
    def __init__(self, channel_ID, timeout):
        super().__init__()
        self.channel_ID = channel_ID
        self.timeout = timeout

    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(content=f"Whoops, you took too long to make a desicion. I've disabled all the buttons.\nRun the command again if you want to edit the channel again", view=self)
    
    @discord.ui.button(label="Yes", row=0, style=discord.ButtonStyle.danger)
    async def first_button_callback(self, button, interaction):
        with db.atomic() as txn:
            GuildSettings.update(ChannelID=self.channel_ID).where(GuildSettings.ServerID == interaction.message.guild.id).execute()
        self.disable_all_items()
        # Ends the interaction timeout to prevent on_timeout from being called
        self.stop()
        await interaction.response.edit_message(content="Alright, the channel has been updated", view=self)

    @discord.ui.button(label="No", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        self.disable_all_items()
        # Ends the interaction timeout to prevent on_timeout from being called
        self.stop()
        await interaction.response.edit_message(content="Alright, no changes have been made", view=self)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_guild_remove(guild: discord.Guild):
    with db.atomic() as txn:
        GuildSettings.delete().where(GuildSettings.ServerID == guild.id).execute()

@bot.slash_command(name="setup", description="Set the channel where the bot will send the messages")
@discord.default_permissions(manage_messages=True)
async def global_command(ctx: discord.ApplicationContext, channel: discord.TextChannel): 
        if GuildSettings.get_or_none(ServerID=ctx.guild.id) is None:
            webhook = await channel.create_webhook(name="Don't Be Like This Bot")
            with db.atomic() as txn:    
                GuildSettings.create(ServerID=ctx.guild.id, ChannelID=channel.id, WebHookURL=webhook.url)
            await ctx.respond(f"Set the channel to <#{channel.id}>!", ephemeral=True)
        else:
            await ctx.respond(f"It looks like you already have a channel set for messages.\nWould you like to update it?", view=YesOrNoButtons(timeout=20, channel_ID=channel.id), ephemeral=True) 

@bot.message_command(name="Don't be like this")
@discord.default_permissions(manage_messages=True)
async def dont_be_like_this(ctx: discord.ApplicationContext, message: discord.Message):  
    if ctx.guild is None:
        await ctx.send_response(f"You cannot use this command in DMs!", ephemeral=True)
        return
    if ctx.author.id == bot.user.id:
        await ctx.send_response(f"I can't clown on my own messages!", ephemeral=True)
        return
    if message.author.bot:
        await ctx.send_response(f"I can't clown on other bots!", ephemeral=True)
        return
    webhook_url = GuildSettings.get_or_none(GuildSettings.ServerID == ctx.guild.id)
    if webhook_url is None:
        await ctx.send_response(f"You cannot use the bot without setting it up first! Run the /setup command to set the bot up!", ephemeral=True)
        return
    webhook_url = webhook_url.WebHookURL

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(content=f'[[Original Message](<{message.jump_url}>)] {message.content}', username=f'🤡{message.author.name}', avatar_url=message.author.avatar.url, allowed_mentions=discord.AllowedMentions.none())
    await ctx.send_response(f"🤡 <@{message.author.id}>", ephemeral=True)

bot.run(discord_token)