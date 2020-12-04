from typing import List

from discord import Message


class Round:
    _messages: List[Message] = []

    def __init__(self, message: Message):
        self._messages = [message]
