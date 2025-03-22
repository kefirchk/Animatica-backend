from unittest.mock import AsyncMock, MagicMock

import pytest
from src.domain.usecases import UserSignUpUseCase
from src.domain.usecases.auth.send_confirmation_email import (
    SendConfirmationEmailUseCase,
)
from src.infrastructure.exceptions import UserExistsException
from starlette.responses import JSONResponse


@pytest.mark.asyncio
class TestUserSignUpUseCase:
    async def test_user_sign_up_success(self, mock_db_repository, mock_keycloak_repository):
        mock_send_email_use_case = AsyncMock()
        mock_db_repository.get_user_by_email.return_value = None
        mock_keycloak_repository.sign_up.return_value = "new_user_sub"
        mock_db_repository.create_user = AsyncMock()
        use_case = UserSignUpUseCase(
            keycloak_repository=mock_keycloak_repository,
            db_repository=mock_db_repository,
            email_sender=AsyncMock(),
            send_email_use_case=mock_send_email_use_case,
        )
        request = use_case.Request(email="test@example.com", password="password", name="Test User")
        response = await use_case.execute(request)

        assert not response
        mock_db_repository.get_user_by_email.assert_called_once_with("test@example.com")
        mock_keycloak_repository.sign_up.assert_called_once_with("test@example.com", "password", "Test User")
        mock_db_repository.create_user.assert_called_once_with("new_user_sub", "Test User", "test@example.com")
        mock_send_email_use_case.execute.assert_called_once_with(
            SendConfirmationEmailUseCase.Request(recipient="test@example.com")
        )

    async def test_user_sign_up_email_already_exists(self, mock_db_repository, mock_keycloak_repository):
        mock_send_email_use_case = AsyncMock()
        mock_db_repository.get_user_by_email.return_value = MagicMock()
        use_case = UserSignUpUseCase(
            keycloak_repository=mock_keycloak_repository,
            db_repository=mock_db_repository,
            email_sender=AsyncMock(),
            send_email_use_case=mock_send_email_use_case,
        )
        request = use_case.Request(email="test@example.com", password="password", name="Test User")
        response = await use_case.execute(request)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 409
        assert "UserExistsException" in response.body.decode()
        mock_db_repository.get_user_by_email.assert_called_once_with("test@example.com")
        mock_keycloak_repository.sign_up.assert_not_called()
        mock_db_repository.create_user.assert_not_called()
        mock_send_email_use_case.execute.assert_not_called()

    async def test_user_sign_up_error_in_email_sending(self, mock_db_repository, mock_keycloak_repository):
        mock_send_email_use_case = AsyncMock()
        mock_db_repository.get_user_by_email.return_value = None
        mock_keycloak_repository.sign_up.return_value = "new_user_sub"
        mock_db_repository.create_user = AsyncMock()
        mock_send_email_use_case.execute.side_effect = Exception("Email sending failed")
        use_case = UserSignUpUseCase(
            keycloak_repository=mock_keycloak_repository,
            db_repository=mock_db_repository,
            email_sender=AsyncMock(),
            send_email_use_case=mock_send_email_use_case,
        )
        request = use_case.Request(email="test@example.com", password="password", name="Test User")
        response = await use_case.execute(request)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        assert "Email sending failed" in response.body.decode()
        mock_db_repository.get_user_by_email.assert_called_once_with("test@example.com")
        mock_keycloak_repository.sign_up.assert_called_once_with("test@example.com", "password", "Test User")
        mock_db_repository.create_user.assert_called_once_with("new_user_sub", "Test User", "test@example.com")
        mock_send_email_use_case.execute.assert_called_once_with(
            SendConfirmationEmailUseCase.Request(recipient="test@example.com")
        )
