from discord import DMChannel, User
from discord import Message

from stummtaube import main
from stummtaube.commands import START, JOIN
from stummtaube.data.game import players
from stummtaube.data.rounds import create_round, get_round_for_reply, add_new_message


async def handle_message(message: Message) -> None:
    if not isinstance(message.channel, DMChannel) or message.author == main.client:
        return

    if existing_round := get_round_for_reply(message):
        await add_new_message(existing_round, message)
    elif message.content == JOIN:
        join_player(message.author)
    elif message.content.startswith(START) and message.author in players:
        await create_round(message)


def join_player(author: User):
    players.add(author)
