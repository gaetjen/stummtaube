import random
from typing import List

from discord import Message, User, TextChannel

from stummtaube.commands import START
from stummtaube.data.game import players


class Round:
    def __init__(self):
        self._user_messages: List[Message] = []
        self._forwarded_messages: List[Message] = []

    async def forward_last_message(self):
        recipient: User = self._get_next_player()
        raw_content = self._user_messages[-1].content
        forwarded_content = raw_content.split(START, 1)[1].strip() if len(self._user_messages) == 1 else raw_content
        if not forwarded_content:
            forwarded_content = self._user_messages[-1].attachments[0].url
        self._forwarded_messages.append(await recipient.send(forwarded_content))

    async def add_new_message(self, message: Message):
        self._user_messages.append(message)
        await self.forward_last_message()

    def get_key(self) -> int:
        return self._forwarded_messages[-1].id

    # will need to look at message history to select a good recipient
    def _get_next_player(self) -> User:
        return random.sample(players, 1)[0]

    async def end(self, channel: TextChannel):
        for message in self._forwarded_messages:
            await channel.send(message.content, tts=True)
