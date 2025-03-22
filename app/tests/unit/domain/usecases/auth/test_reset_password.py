import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from src.domain.usecases.auth.reset_password import ResetPasswordUseCase
from src.infrastructure.exceptions import InvalidTokenException
from starlette.responses import JSONResponse


class TestResetPasswordUseCase:
    @pytest.mark.asyncio
    async def test_reset_password_success(self, mock_db_repository, mock_keycloak_repository):
        mock_email_sender = AsyncMock()
        mock_token_handler = MagicMock()
        mock_token_handler.decode_token.return_value = {"email": "test@example.com"}
        mock_db_repository.get_user_by_email.return_value = MagicMock(sub="user_sub_id")
        mock_keycloak_repository.login.return_value = {
            "refresh_token": "new_refresh_token",
            "access_token": "new_access_token",
            "expires_in": 3600,
            "refresh_expires_in": 7200,
        }
        use_case = ResetPasswordUseCase(
            email_sender=mock_email_sender,
            token_handler=mock_token_handler,
            db_repository=mock_db_repository,
            keycloak_repository=mock_keycloak_repository,
        )
        response = await use_case.execute(use_case.Request(token="valid_token", password="new_password"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        response_data = json.loads(response.body.decode())
        assert response_data["refresh_token"] == "new_refresh_token"
        assert response_data["access_token"] == "new_access_token"
        assert response_data["expires_in"] == 3600
        assert response_data["refresh_expires_in"] == 7200
        mock_token_handler.decode_token.assert_called_once_with("valid_token")
        mock_db_repository.get_user_by_email.assert_called_once_with("test@example.com")
        mock_keycloak_repository.set_password.assert_called_once_with("user_sub_id", "new_password")
        mock_keycloak_repository.login.assert_called_once_with("test@example.com", "new_password")

    @pytest.mark.asyncio
    async def test_reset_password_user_not_found(self, mock_db_repository, mock_keycloak_repository):
        mock_email_sender = AsyncMock()
        mock_token_handler = MagicMock()
        mock_token_handler.decode_token.return_value = {"email": "test@example.com"}
        mock_db_repository.get_user_by_email.return_value = None
        use_case = ResetPasswordUseCase(
            email_sender=mock_email_sender,
            token_handler=mock_token_handler,
            db_repository=mock_db_repository,
            keycloak_repository=mock_keycloak_repository,
        )
        response = await use_case.execute(use_case.Request(token="valid_token", password="new_password"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 404
        assert "User with this email does not exist" in response.body.decode()
        mock_token_handler.decode_token.assert_called_once_with("valid_token")
        mock_db_repository.get_user_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_reset_password_invalid_token(self, mock_db_repository, mock_keycloak_repository):
        mock_email_sender = AsyncMock()
        mock_token_handler = MagicMock()
        mock_token_handler.decode_token.side_effect = InvalidTokenException("Invalid token")
        use_case = ResetPasswordUseCase(
            email_sender=mock_email_sender,
            token_handler=mock_token_handler,
            db_repository=mock_db_repository,
            keycloak_repository=mock_keycloak_repository,
        )
        response = await use_case.execute(use_case.Request(token="invalid_token", password="new_password"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 401
        assert "Invalid token" in response.body.decode()
        mock_token_handler.decode_token.assert_called_once_with("invalid_token")
