from unittest.mock import Mock, PropertyMock, patch

import pytest
from discord import TextChannel, DMChannel

from stummtaube.main import client
from stummtaube.message_handler import handle_message


@pytest.mark.asyncio
async def test_text_channel_should_not_be_processed():
    mock_message = Mock()
    channel_mock = PropertyMock(TextChannel)
    type(mock_message).channel = channel_mock
    content_mock = PropertyMock()
    type(mock_message).content = content_mock

    await handle_message(mock_message)

    content_mock.assert_not_called()


@pytest.mark.asyncio
async def test_messages_from_bot_should_not_be_processed():
    mock_message = Mock()
    mock_message.author = client
    type(mock_message).channel = PropertyMock(DMChannel)
    content_mock = PropertyMock()
    type(mock_message).content = content_mock

    await handle_message(mock_message)

    content_mock.assert_not_called()


@pytest.mark.asyncio
@patch("stummtaube.message_handler.join_player")
async def test_join_adds_user(join_player):
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "!join"

    await handle_message(mock_message)

    join_player.assert_called_with(mock_message.author)


@pytest.mark.asyncio
@patch("stummtaube.message_handler.create_round")
async def test_start_does_not_start_round_when_player_is_not_joined(mock_create):
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "!start Grünes Zebra"

    await handle_message(mock_message)

    mock_create.assert_not_called()


@patch("stummtaube.message_handler.create_round")
@pytest.mark.asyncio
async def test_start_creates_round(mock_create):
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "!start Grünes Zebra"

    with patch("stummtaube.message_handler.players", {mock_message.author}):
        await handle_message(mock_message)
        mock_create.assert_called_with(mock_message)


@patch("stummtaube.message_handler.join_player")
@patch("stummtaube.message_handler.create_round")
@pytest.mark.asyncio
async def test_no_command_falls_through(mock_create, join_player):
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "Ich bin eine Biene!"

    await handle_message(mock_message)

    mock_create.assert_not_called()
    join_player.assert_not_called()

