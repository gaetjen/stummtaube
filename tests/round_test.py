from unittest.mock import Mock

from stummtaube.data.round import Round


def test_created_round_has_message():
    message = Mock()
    new_round = Round(message)
    assert message in new_round._messages
    assert len(new_round._messages) == 1
