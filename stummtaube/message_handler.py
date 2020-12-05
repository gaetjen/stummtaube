from discord import DMChannel, User
from discord import Message

import stummtaube.data.rounds as rounds_management
from stummtaube import main
from stummtaube.commands import START, JOIN, END
from stummtaube.data.game import players
from stummtaube.data.round import Round


async def handle_message(message: Message) -> None:
    if not isinstance(message.channel, DMChannel) or message.author == main.client:
        return

    if existing_round := rounds_management.get_round_for_reply(message):
        await handle_reply(existing_round, message)
    elif message.content == JOIN:
        join_player(message.author)
    elif message.content.startswith(START) and message.author in players:
        await rounds_management.create_round(message)


async def handle_reply(existing_round: Round, message: Message) -> None:
    if message.content == END:
        await rounds_management.end_round(existing_round)
    else:
        await rounds_management.add_new_message(existing_round, message)


def join_player(author: User) -> None:
    players.add(author)
