from pytest_mock import MockerFixture

import build_user_data


def test_load_users(mocker: MockerFixture) -> None:
    mocker.patch(
        "build_user_data.open",
        mocker.mock_open(read_data="username\nuser1\nuser2"),
    )
    assert build_user_data.load_users() == {"user1", "user2"}
