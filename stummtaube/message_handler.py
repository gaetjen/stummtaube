from discord import Message
from discord import DMChannel
from stummtaube.data.game import players, rounds
from stummtaube.data.round import Round


def handle_message(message: Message) -> None:
    if not isinstance(message.channel, DMChannel):
        return

    if message.content == "!join":
        players.add(message.author)
    elif message.content.startswith("!start") and message.author in players:
        rounds.append(Round(message))
