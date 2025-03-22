from unittest.mock import AsyncMock, MagicMock

import pytest
from src.domain.usecases.auth.forgot_password import ForgotPasswordUseCase
from starlette.responses import JSONResponse


class TestForgotPasswordUseCase:
    @pytest.mark.asyncio
    async def test_forgot_password_success(self, mock_db_repository):
        mock_email_sender = AsyncMock()
        mock_token_handler = MagicMock()
        mock_user = AsyncMock()
        mock_user.name = "Test User"
        mock_db_repository.get_user_by_email.return_value = mock_user
        mock_token_handler.generate_token.return_value = "mock_token"
        use_case = ForgotPasswordUseCase(
            email_sender=mock_email_sender, token_handler=mock_token_handler, db_repository=mock_db_repository
        )
        response = await use_case.execute(use_case.Request(email="test@example.com"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        mock_db_repository.get_user_by_email.assert_called_once_with("test@example.com")
        mock_token_handler.generate_token.assert_called_once_with("test@example.com")
        mock_email_sender.send_password_reset_email.assert_called_once_with(
            "test@example.com", "mock_token", "Test User"
        )

    @pytest.mark.asyncio
    async def test_forgot_password_user_not_found(self, mock_db_repository):
        mock_email_sender = AsyncMock()
        mock_token_handler = AsyncMock()
        mock_db_repository.get_user_by_email.return_value = None
        use_case = ForgotPasswordUseCase(
            email_sender=mock_email_sender, token_handler=mock_token_handler, db_repository=mock_db_repository
        )
        response = await use_case.execute(use_case.Request(email="notfound@example.com"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 404
        assert "User with this email does not exist" in response.body.decode()

    @pytest.mark.asyncio
    async def test_forgot_password_email_send_failure(self, mock_db_repository):
        mock_email_sender = AsyncMock()
        mock_token_handler = AsyncMock()
        mock_db_repository.get_user_by_email.return_value = MagicMock(name="Test User")
        mock_token_handler.generate_token.return_value = "mock_token"
        mock_email_sender.send_password_reset_email.side_effect = Exception("Email send failure")
        use_case = ForgotPasswordUseCase(
            email_sender=mock_email_sender, token_handler=mock_token_handler, db_repository=mock_db_repository
        )
        response = await use_case.execute(use_case.Request(email="test@example.com"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        assert "Email send failure" in response.body.decode()
