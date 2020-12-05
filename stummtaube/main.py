import logging
import os

from discord import Client, Message, Guild

from stummtaube import message_handler
from stummtaube.data.game import get_channel

client: Client = Client()


@client.event
async def on_ready() -> None:
    logging.info('We have logged in as {0.user}'.format(client))


@client.event
async def on_guild_available(guild: Guild):
    await get_channel(guild)


@client.event
async def on_message(message: Message) -> None:
    logging.debug("on_message called for: " + message.content)
    await message_handler.handle_message(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client.run(os.environ['DISCORD_TOKEN'])
