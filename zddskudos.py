import discord
import SECRETS
import settings
import kudos_handler
import random
import extras


### This is executed as soon as the bot is started!
# -> Set Game to "kudos++"
# -> Set status to online
@settings.client.event
async def on_ready():
    # initial print messages
    print("Ready!")
    for s in settings.client.guilds:
        print(" - %s (%s)" % (s.name, s.id))
        roles = s.roles

    for allRoles in roles:
        if allRoles.id == 694500490142285825:
            role = allRoles

    # Set Game and status
    await settings.client.change_presence(status=discord.Status.online, activity=discord.Game(name='kudos++'))

    while True:
        randomR = random.randint(1,255)
        randomG = random.randint(1,255)
        randomB = random.randint(1,255)
        newColor = discord.Color.from_rgb(randomR, randomG, randomB)
        await role.edit(colour=newColor)


@settings.client.event
async def on_member_join(member):
    # log-channel message
    channel = settings.client.get_channel(694419632467214410)
    await extras.send_msg(channel, "{} joined the server!".format(member.name))


### This is executed if someone leaves the server!
# -> sending status-message to log-channel
@settings.client.event
async def on_member_remove(member):
    # log-channel message
    channel = settings.client.get_channel(694419632467214410)
    await extras.send_msg(channel, "{} left the server!".format(member.display_name))


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
