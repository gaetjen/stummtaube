import random
from typing import List

from discord import Message, User

from stummtaube.commands import START
from stummtaube.data.game import players


class Round:
    _messages: List[Message] = []

    def __init__(self, message: Message):
        self._messages = [message]
        self.forward_message(message)

    def forward_message(self, message: Message):
        recipient: User = self.__get_next_player()
        recipient.send(message.content.split(START, 1)[1].strip())

    # will need to look at message history to select a good recipient
    def __get_next_player(self) -> User:
        return random.sample(players, 1)[0]


rounds: List[Round] = []
