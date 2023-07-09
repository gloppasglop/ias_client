import pytest
import ias_client

import jwt
from datetime import datetime, timezone, timedelta


def generate_valid_token(payload):
    return jwt.encode({"exp": datetime.now(tz=timezone.utc)+timedelta(days=10),'payload': payload}, "secret") 

def generate_expired_token(payload):
    return jwt.encode({"exp": datetime.now(tz=timezone.utc)+timedelta(days=-10),'payload': payload}, "secret") 

@pytest.fixture
def mock_get_tokens(mocker):
    yield mocker.patch('ias_client.Connection._get_tokens')

def test_authenticate_no_token(mock_get_tokens):

    expected_access_token = generate_valid_token('access')
    expected_refresh_token =  generate_valid_token('refresh')

    mock_get_tokens.return_value = {
            'access_token': expected_access_token,
            'refresh_token': expected_refresh_token
    }

    conn = ias_client.Connection(username="toto",password="tutu")

    tokens = conn.authenticate()

    # _get_tokens should e called once
    mock_get_tokens.assert_called_once()
    assert 'access_token' in tokens
    assert 'refresh_token' in tokens
    assert tokens['access_token'] == expected_access_token
    assert tokens['refresh_token'] == expected_refresh_token

    assert 'access_token' in conn._tokens
    assert 'refresh_token' in conn._tokens

    assert conn._tokens['refresh_token'] == expected_refresh_token
    assert conn._tokens['access_token'] == expected_access_token



def test_authenticate_with_valid_access_token(mock_get_tokens):

    expected_access_token = generate_valid_token('valid_access')
    expected_refresh_token = generate_valid_token('valid_token')

    mock_get_tokens.return_value = {
            'access_token':  generate_valid_token('new_valid_access'),
            'refresh_token': generate_valid_token('new_valid_refresh')
    }

    conn = ias_client.Connection(username="toto",password="tutu")
    # Set an existing token
    conn._tokens = {
            'access_token': expected_access_token,
            'refresh_token': expected_refresh_token
    }

    tokens = conn.authenticate()

    mock_get_tokens.assert_not_called()
    # We should still get the original token
    assert tokens['access_token'] == expected_access_token
    assert tokens['refresh_token'] == expected_refresh_token

    # We should still get the original token
    assert conn._tokens['refresh_token'] == expected_refresh_token
    assert conn._tokens['access_token'] == expected_access_token

def test_authenticate_with_expired_access_token(mock_get_tokens):

    expired_access_token = generate_expired_token('expired_token')
    expired_refresh_token = generate_expired_token('expired_token')


    conn = ias_client.Connection(username="toto",password="tutu")
    # Set an existing expired token
    conn._tokens = {
            'access_token': expired_access_token,
            'refresh_token': expired_refresh_token
    }

    expected_access_token =  generate_valid_token('new_valid_access')
    expected_refresh_token =  generate_valid_token('new_valid_refresh')

    mock_get_tokens.return_value = {
            'access_token':  expected_access_token,
            'refresh_token': expected_refresh_token
    }
    tokens = conn.authenticate()

    mock_get_tokens.assert_called_once()
    # We should still get the original token
    assert tokens['access_token'] == expected_access_token
    assert tokens['refresh_token'] == expected_refresh_token

    # We should still get the original token
    assert conn._tokens['refresh_token'] == expected_refresh_token

