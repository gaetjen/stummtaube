from discord import DMChannel
from discord import Message

from stummtaube.commands import START, JOIN
from stummtaube.data.game import players
from stummtaube.data.round import Round, rounds


async def handle_message(message: Message) -> None:
    if not isinstance(message.channel, DMChannel):
        return

    if message.content == JOIN:
        players.add(message.author)
    elif message.content.startswith(START) and message.author in players:
        new_round = Round(message)
        await new_round.forward_message()
        rounds.append(new_round)
