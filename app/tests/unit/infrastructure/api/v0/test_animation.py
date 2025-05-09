from unittest.mock import AsyncMock

import pytest
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.animation import AnimateImageByVideoUseCase


class TestAPIAnimation:
    @pytest.fixture
    def setup_jwt_bearer(self, mocker):
        mock_jwt_bearer = mocker.patch(
            "src.infrastructure.api.v0.animation.JWTBearer.__call__", return_value=UserAuthInfo(sub_id="1")
        )
        return mock_jwt_bearer

    @pytest.mark.asyncio
    async def test__animate_image_by_video__success(self, mocker, api_client, setup_jwt_bearer):
        mock_execute = mocker.patch.object(
            AnimateImageByVideoUseCase,
            "execute",
            new_callable=AsyncMock,
            return_value=b"test-data",
        )

        response = await api_client.post(
            "/api/v0/animation/video",
            headers={"Authorization": "Bearer mocked_token"},
            files={"source_image": b"aaa", "driving_video": b"bbb"},
        )

        assert response.status_code == 200
        assert response.json() == "test-data"
        setup_jwt_bearer.assert_called_once()
        mock_execute.assert_called_once()
