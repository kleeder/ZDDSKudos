import discord
import SECRETS
import settings
import kudos_handler


### This is executed as soon as the bot is started!
# -> Set Game to "kudos++"
# -> Set status to online
@settings.client.event
async def on_ready():
    # initial print messages
    print("Ready!")
    for s in settings.client.guilds:
        print(" - %s (%s)" % (s.name, s.id))

    # Set Game and status
    await settings.client.change_presence(status=discord.Status.online, activity=discord.Game(name='kudos++'))


### This is executed on a new incoming message!
# -> Handles most of the bot's functionality (aka the kudos)
@settings.client.event
async def on_message(message):
    # check if the message was sent in a private chat
    privateChat = message.channel.type[0] == "private"

    # check if the message author is bot himself
    byBot = message.author.bot

    # check for specific roles
    if not privateChat:
        try:
            kudoBan = "kudo-ban" in [y.name.lower() for y in message.author.roles]
        except:
            kudoBan = False
    else:
        kudoBan = False

   # now for the general react-stuff
    if not byBot and not privateChat:
        # time to check for commands if there is no file or image attached to the message
        if len(message.attachments) < 1:
            msgLower = message.content.lower()
            try:
                cmd = msgLower.split()[0]
            except:
                cmd = msgLower

            ### KUDOS-STUFF
            if not kudoBan:
                await kudos_handler.kudos_handler(msgLower, message)

            if cmd[:6] == "!kudos":
                await kudos_handler.kudos_command(cmd, msgLower, message)

# initialize
settings.client.run(SECRETS.TOKEN)
