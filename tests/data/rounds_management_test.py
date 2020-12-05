from unittest.mock import Mock, patch, MagicMock, AsyncMock

import pytest
from aiohttp.web_exceptions import HTTPBadGateway

from stummtaube.data.round import Round
from stummtaube.data.rounds import create_round, rounds, get_round_for_reply, add_new_message


# TODO: split
@pytest.mark.asyncio
async def test_created_round_has_message_and_sends_it():
    user_mock = MagicMock()
    user_mock.send = AsyncMock()
    with patch("stummtaube.data.round.players", {user_mock}):
        message = Mock()
        message.content = "!start Bierschiss"

        await create_round(message)

        assert message in next(iter(rounds.values()))._user_messages
        assert len(next(iter(rounds.values()))._user_messages) == 1
        user_mock.send.assert_called_with("Bierschiss")


def test_non_reply_message_gets_no_round():
    message_mock = Mock()
    message_mock.reference = None
    assert get_round_for_reply(message_mock) is None


def test_get_none_if_no_round_with_id_exists():
    message_mock = Mock()
    message_mock.reference.message_id = 123
    with patch("stummtaube.data.rounds.rounds", {321: Mock()}):
        assert get_round_for_reply(message_mock) is None


def test_get_round_with_matching_id():
    message_mock = Mock()
    message_mock.reference.message_id = 123
    with patch("stummtaube.data.rounds.rounds", {123: Mock()}):
        assert get_round_for_reply(message_mock) is not None


@pytest.mark.asyncio
async def test_add_new_message_updates_rounds():
    round_mock = AsyncMock()
    round_mock.get_key = Mock(side_effect=[567, 890])
    with patch("stummtaube.data.rounds.rounds", {567: Mock()}) as mocked_rounds:
        await add_new_message(round_mock, Mock())
        assert mocked_rounds[890] is not None
        assert mocked_rounds.get(567) is None


@pytest.mark.asyncio
async def test_add_new_message_does_not_update_rounds_on_error():
    round_mock = AsyncMock()
    round_mock.get_key = Mock(side_effect=HTTPBadGateway())
    with patch("stummtaube.data.rounds.rounds", {567: Mock()}) as mocked_rounds:
        try:
            await add_new_message(round_mock, Mock())
            assert False
        except HTTPBadGateway:
            assert mocked_rounds[567] is not None
