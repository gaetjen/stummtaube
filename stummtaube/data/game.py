import os
from typing import Set, Optional

from discord import User, Guild, TextChannel

players: Set[User] = set()

results_channel: Optional[TextChannel] = None


async def get_channel(guild: Guild) -> None:
    global results_channel
    results_channel = guild.get_channel(int(os.environ['RESOLUTION_CHANNEL_ID']))
    await results_channel.send("cheep cheep I'm a bot", tts=True)
