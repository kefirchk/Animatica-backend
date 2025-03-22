import json

import pytest
from src.domain.usecases.auth.refresh_tokens import RefreshTokensUseCase
from src.infrastructure.exceptions import InvalidTokenException
from starlette.responses import JSONResponse


class TestRefreshTokensUseCase:
    @pytest.mark.asyncio
    async def test_refresh_tokens_success(self, mock_keycloak_repository):
        mock_keycloak_repository.refresh_token.return_value = {
            "refresh_token": "new_refresh_token",
            "access_token": "new_access_token",
            "expires_in": 3600,
            "refresh_expires_in": 7200,
        }
        use_case = RefreshTokensUseCase(repository=mock_keycloak_repository)
        response = await use_case.execute(use_case.Request(refresh_token="old_refresh_token"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        response_data = json.loads(response.body.decode())
        assert response_data["refresh_token"] == "new_refresh_token"
        assert response_data["access_token"] == "new_access_token"
        assert response_data["expires_in"] == 3600
        assert response_data["refresh_expires_in"] == 7200
        mock_keycloak_repository.refresh_token.assert_called_once_with("old_refresh_token")

    @pytest.mark.asyncio
    async def test_refresh_tokens_failure(self, mock_keycloak_repository):
        mock_keycloak_repository.refresh_token.side_effect = InvalidTokenException("Invalid refresh token")
        use_case = RefreshTokensUseCase(repository=mock_keycloak_repository)
        response = await use_case.execute(use_case.Request(refresh_token="invalid_refresh_token"))

        assert isinstance(response, JSONResponse)
        assert response.status_code == 401
        assert "Invalid refresh token" in response.body.decode()
        mock_keycloak_repository.refresh_token.assert_called_once_with("invalid_refresh_token")
