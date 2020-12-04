from unittest.mock import Mock, patch, MagicMock

from stummtaube.data.round import Round


def test_created_round_has_message_and_sends_it():
    user_mock = MagicMock()
    user_mock.send = MagicMock()
    with patch("stummtaube.data.round.players", {user_mock}):
        message = Mock()
        message.content = "!start Bierschiss"
        new_round = Round(message)
        assert message in new_round._messages
        assert len(new_round._messages) == 1
        user_mock.send.assert_called_with("Bierschiss")
