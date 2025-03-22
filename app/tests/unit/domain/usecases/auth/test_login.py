import json
from unittest.mock import AsyncMock

import pytest
from keycloak import KeycloakError
from src.domain.usecases import UserLoginUseCase
from src.infrastructure.exceptions import InvalidCredentialsException
from starlette.responses import JSONResponse


class TestUserLoginUseCase:
    @pytest.mark.asyncio
    async def test_user_login_success(self, mock_keycloak_repository):
        mock_keycloak_repository.login.return_value = {
            "refresh_token": "mock_refresh_token",
            "access_token": "mock_access_token",
            "expires_in": 3600,
            "refresh_expires_in": 7200,
        }
        use_case = UserLoginUseCase(repository=mock_keycloak_repository)
        response = await use_case.execute(use_case.Request(username="test_user", password="test_password"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        mock_keycloak_repository.login.assert_called_once_with("test_user", "test_password")
        response_data = json.loads(response.body.decode())
        assert response_data["refresh_token"] == "mock_refresh_token"
        assert response_data["access_token"] == "mock_access_token"
        assert response_data["expires_in"] == 3600
        assert response_data["refresh_expires_in"] == 7200

    @pytest.mark.asyncio
    async def test_user_login_failure(self, mock_keycloak_repository):
        mock_keycloak_repository.login.side_effect = InvalidCredentialsException("Invalid credentials")
        use_case = UserLoginUseCase(repository=mock_keycloak_repository)
        response = await use_case.execute(use_case.Request(username="wrong-user", password="wrong-password"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 401
        assert "Invalid credentials" in response.body.decode()
        mock_keycloak_repository.login.assert_called_once_with("wrong-user", "wrong-password")
