from unittest.mock import Mock, PropertyMock, patch, MagicMock

from discord import TextChannel, DMChannel

from stummtaube.message_handler import handle_message


def test_text_channel_should_not_be_processed():
    mock_message = Mock()
    channel_mock = PropertyMock(TextChannel)
    type(mock_message).channel = channel_mock
    content_mock = PropertyMock()
    type(mock_message).content = content_mock

    handle_message(mock_message)

    content_mock.assert_not_called()


@patch("stummtaube.message_handler.players")
def test_join_adds_user(mocked_players):
    mocked_players.add = MagicMock(name="add to players")
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "!join"
    author_mock = PropertyMock(name="author")
    type(mock_message).author = author_mock

    handle_message(mock_message)

    author_mock.assert_called()
    mocked_players.add.assert_called_with(mock_message.author)


@patch("stummtaube.message_handler.rounds")
def test_start_does_not_start_round_when_player_is_not_joined(mocked_rounds):
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "!start Grünes Zebra"

    handle_message(mock_message)

    assert len(mocked_rounds.method_calls) == 0


@patch("stummtaube.message_handler.Round", MagicMock())
@patch("stummtaube.message_handler.rounds")
def test_start_creates_round(mocked_rounds):
    mocked_rounds.append = MagicMock()
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "!start Grünes Zebra"

    with patch("stummtaube.message_handler.players", {mock_message.author}):
        handle_message(mock_message)
        mocked_rounds.append.assert_called()


@patch("stummtaube.message_handler.players")
@patch("stummtaube.message_handler.rounds")
def test_no_command_falls_through(mocked_rounds, mocked_players):
    mock_message = Mock(name="message")
    mock_message.channel = PropertyMock(DMChannel, name="channel")
    mock_message.content = "Ich bin eine Biene!"

    handle_message(mock_message)

    assert len(mocked_rounds.method_calls) == 0
    assert len(mocked_players.method_calls) == 0

