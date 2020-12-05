from unittest.mock import Mock, patch, MagicMock, AsyncMock

import pytest

from stummtaube.data.round import Round, create_round, rounds


@pytest.mark.asyncio
async def test_created_round_has_message_and_sends_it():
    user_mock = MagicMock()
    user_mock.send = AsyncMock()
    with patch("stummtaube.data.round.players", {user_mock}):
        message = Mock()
        message.content = "!start Bierschiss"

        await create_round(message)

        assert message in rounds[0]._messages
        assert len(rounds[0]._messages) == 1
        user_mock.send.assert_called_with("Bierschiss")
