from typing import Optional, Dict

from discord import Message

import stummtaube.data.game
from stummtaube.data.round import Round

rounds: Dict[int, Round] = {}


async def create_round(message: Message) -> None:
    new_round = Round()
    await new_round.add_new_message(message)
    _add_round(new_round)


def get_round_for_reply(message: Message) -> Optional[Round]:
    if (ref := message.reference) is not None:
        return rounds.get(ref.message_id)
    else:
        return None


async def add_new_message(existing_round: Round, message: Message) -> None:
    old_key = existing_round.get_key()
    await existing_round.add_new_message(message)
    del rounds[old_key]
    _add_round(existing_round)


async def end_round(existing_round: Round) -> None:
    old_key = existing_round.get_key()
    await existing_round.end(stummtaube.data.game.results_channel)
    del rounds[old_key]


def _add_round(round_to_add: Round) -> None:
    rounds[round_to_add.get_key()] = round_to_add

