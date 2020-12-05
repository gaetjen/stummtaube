import random
from typing import List

from discord import Message, User

from stummtaube.commands import START
from stummtaube.data.game import players


class Round:
    _messages: List[Message] = []
    _last_message: Message = None

    async def forward_last_message(self):
        recipient: User = self.__get_next_player()
        raw_content = self._messages[-1].content
        forwarded_content = raw_content.split(START, 1)[1].strip() if len(self._messages) == 1 else raw_content
        self._last_message = await recipient.send(forwarded_content)

    async def add_new_message(self, message: Message):
        self._messages.append(message)
        await self.forward_last_message()

    def get_key(self) -> int:
        return self._last_message.id

    # will need to look at message history to select a good recipient
    def __get_next_player(self) -> User:
        return random.sample(players, 1)[0]
