from discord import Message
from discord import DMChannel
from stummtaube.data.game import players


def handle_message(message: Message) -> None:
    if not isinstance(message.channel, DMChannel):
        return

    if message.content == "!join":
        players.add(message.author)
