import extras
import random
import itertools
import asyncio

async def kudos_handler(msg, message):
    # additional 56-exception
    if msg == "56++" or msg == "56--":
        await extras.send_msg(message.channel, "**56 has 56 kudos.**")
    # positive kudos
    elif len(msg) < 35 and msg.endswith("++"):
        kudomsg = msg[:-2]
        kudomsg = kudomsg.rstrip().lstrip()
        kudos = extras.read_kudos()
        if not kudomsg in kudos:
            kudos[kudomsg] = 0
        kudos[kudomsg] += 1
        kudosAmount = kudos[kudomsg]
        await extras.send_msg(message.channel, "**{} has {} kudos.**".format(str(message.content)[:-2], kudosAmount))
        extras.dump_kudos(kudos)
    # negative kudos
    elif len(msg) < 35 and msg.endswith("--"):
        kudomsg = msg[:-2]
        kudomsg = kudomsg.rstrip().lstrip()
        kudos = extras.read_kudos()
        if not kudomsg in kudos:
            kudos[kudomsg] = 0
        kudos[kudomsg] -= 1
        kudosAmount = kudos[kudomsg]
        await extras.send_msg(message.channel, "**{} has {} kudos.**".format(str(message.content)[:-2], kudosAmount))
        extras.dump_kudos(kudos)
    # kudos too big
    elif len(msg) > 35 and msg.endswith("++") or len(msg) > 35 and msg.endswith("--"):
        await extras.send_msg(message.channel, "**kudos max length : 32**")


async def kudos_command(cmd, msg, message):
    # returns a message with the amount of a specific key
    if cmd == "!kudos":
        try:
            kudos = extras.read_kudos()
            if msg == "!kudos":
                kudosAmount = kudos[""]
                kudosnameReal = ""
            else:
                kudoname = msg.split(' ', 1)[1]
                kudosAmount = kudos[kudoname]
                kudosnameReal = message.content.split(' ', 1)[1]
            await extras.send_msg(message.channel, "**{} has {} kudos.**".format(kudosnameReal, kudosAmount))
        except:
            try:
                kudosnameReal = message.content.split(' ', 1)[1]
                await extras.send_msg(message.channel, "**{} has no <3**".format(kudosnameReal))
            except:
                await extras.send_msg(message.channel, "Something ... went wrong??")

    # returns the kudosboard (top 5 and worst 5)
    elif cmd == "!kudosboard":
        try:
            kudos = extras.read_kudos()
            await check_kudos_board(kudos, message.channel)
        except:
            await extras.send_msg(message.channel, "Something ... went wrong??")

    # random kudos is taken and thrown into the chat
    elif cmd == "!kudosrandom":
        try:
            kudos = extras.read_kudos()
            choice = random.choice(list(kudos.keys()))
            kudosAmount = kudos[choice]
            await extras.send_msg(message.channel, "**{} has {} kudos.**".format(choice, kudosAmount))
        except:
            await extras.send_msg(message.channel, "Something ... went wrong??")

    elif cmd == "!kudosamount":
        try:
            no_kudos = True
            kudos = extras.read_kudos()
            try:
                kudovalue = msg.split(' ', 1)[1]
                valuecount = [(k, len(list(v))) for k, v in itertools.groupby(sorted(kudos.values()))]
                for x in valuecount:
                    if x[0] == int(kudovalue):
                        no_kudos = False
                        if x[1] == 1:
                            await extras.send_msg(message.channel, "**There is currently 1 key with {} kudos.**".format(kudovalue))
                        else:
                            await extras.send_msg(message.channel, "**There are currently {} different keys with {} kudos.**".format(x[1], kudovalue))
                if no_kudos:
                    await extras.send_msg(message.channel, "**There are currently no keys with {} kudos.**".format(kudovalue))
            except:
                fullkeys = len(kudos)
                await extras.send_msg(message.channel, "**There are currently {} keys total.**".format(fullkeys))
        except:
            await extras.send_msg(message.channel, "Something ... went wrong??")


# kudos-check + sort and top5/worst5 return
async def check_kudos_board(kudos, channel):
    # get all kudos sorted by lowest and highest
    aufwaerts = sorted(kudos.items(), key=lambda kv: kv[1])
    abwaerts = sorted(kudos.items(), key=lambda kv: kv[1], reverse=True)
    # get only top 5 each
    lowTop = aufwaerts[:5]
    highTop = abwaerts[:5]
    # create message
    tab = "**Top 5:**\n"
    for item in highTop:
        tab = tab + "{}: {}\n".format(item[0], item[1])
    tab = tab + "**Worst 5:**\n"
    for item in lowTop:
        tab = tab + "{}: {}\n".format(item[0], item[1])
    await asyncio.ensure_future(extras.send_msg(channel, tab))