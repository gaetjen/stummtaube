import random
from typing import List

from discord import Message, User

from stummtaube.commands import START
from stummtaube.data.game import players


class Round:
    _messages: List[Message] = []

    def __init__(self, message: Message):
        self._messages = [message]

    async def forward_message(self):
        recipient: User = self.__get_next_player()
        await recipient.send(self._messages[-1].content.split(START, 1)[1].strip())

    # will need to look at message history to select a good recipient
    def __get_next_player(self) -> User:
        return random.sample(players, 1)[0]


async def create_round(message: Message):
    new_round = Round(message)
    await new_round.forward_message()
    rounds.append(new_round)

rounds: List[Round] = []
