import json
import asyncio
import settings

# kudos.json stuff
def read_kudos():
    with open('kudos.json', 'r') as f:
        return json.load(f)

def dump_kudos(board):
    with open('kudos.json', 'w') as f:
        json.dump(board, f)

async def send_m(channel, m):
    if len(m) > 2000:
        m1 = m[0:2000]
        m2 = m[2000:]
        await channel.send(m1)
        await channel.send(m2)
    await channel.trigger_typing()
    await asyncio.sleep(0.5)
    return await channel.send(m)

# send the message stuff into the world wide web
@settings.client.event
async def send_msg(channel, msg):
    if isinstance(msg, list):
        for m in msg:
            await send_m(channel, m)
    else:
        return await send_m(channel, msg)