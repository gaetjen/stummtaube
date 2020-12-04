import logging
import os

from discord import Client, Message

from stummtaube import message_handler

client: Client = Client()


@client.event
async def on_ready() -> None:
    logging.info('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message) -> None:
    logging.debug("on_message called for: " + message.content)
    message_handler.handle_message(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client.run(os.environ['DISCORD_TOKEN'])
