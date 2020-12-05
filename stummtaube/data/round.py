import random
from typing import List

from discord import Message, User

from stummtaube.commands import START
from stummtaube.data.game import players


class Round:
    _user_messages: List[Message] = []
    _last_forwarded_message: Message = None

    async def forward_last_message(self):
        recipient: User = self._get_next_player()
        raw_content = self._user_messages[-1].content
        forwarded_content = raw_content.split(START, 1)[1].strip() if len(self._user_messages) == 1 else raw_content
        if not forwarded_content:
            forwarded_content = self._user_messages[-1].attachments[0].url
        self._last_forwarded_message = await recipient.send(forwarded_content)

    async def add_new_message(self, message: Message):
        self._user_messages.append(message)
        await self.forward_last_message()

    def get_key(self) -> int:
        return self._last_forwarded_message.id

    # will need to look at message history to select a good recipient
    def _get_next_player(self) -> User:
        return random.sample(players, 1)[0]
