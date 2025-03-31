import io
from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.generating import (
    GenerateImageByTextUseCase,
    GenerateRandomImageUseCase,
    GenerateRandomVideoUseCase,
    GenerateVideoByImageUseCase,
    GenerateVideoByTextUseCase,
)


class TestAPIGenerating:
    @pytest.fixture
    def setup_jwt_bearer(self, mocker):
        mock_jwt_bearer = mocker.patch(
            "src.infrastructure.api.v0.generating.JWTBearer.__call__", return_value=UserAuthInfo(sub_id="1")
        )
        return mock_jwt_bearer

    @pytest.mark.asyncio
    async def test__generate_video_by_text__success(self, mocker, api_client, setup_jwt_bearer):
        mock_execute = mocker.patch.object(
            GenerateVideoByTextUseCase,
            "execute",
            new_callable=AsyncMock,
            return_value=GenerateVideoByTextUseCase.Response(),
        )

        response = await api_client.get(
            "/api/v0/generating/text-to-video",
            params={"text": "some text"},
            headers={"Authorization": "Bearer mocked_token"},
        )

        assert response.status_code == 200
        assert response.json() == {}
        setup_jwt_bearer.assert_called_once()
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test__generate_video_by_image__success(self, mocker, api_client, setup_jwt_bearer):
        mock_execute = mocker.patch.object(
            GenerateVideoByImageUseCase,
            "execute",
            new_callable=AsyncMock,
            return_value=GenerateVideoByImageUseCase.Response(),
        )
        image_file = UploadFile(filename="test_image.png", file=io.BytesIO(b"fake image data"))

        response = await api_client.post(
            "/api/v0/generating/image-to-video",
            files={"image": (image_file.filename, image_file.file, "image/png")},
            headers={"Authorization": "Bearer mocked_token"},
        )

        assert response.status_code == 200
        assert response.json() == {}
        setup_jwt_bearer.assert_called_once()
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test__generate_image_by_text__success(self, mocker, api_client, setup_jwt_bearer):
        mock_execute = mocker.patch.object(
            GenerateImageByTextUseCase,
            "execute",
            new_callable=AsyncMock,
            return_value=GenerateImageByTextUseCase.Response(),
        )

        response = await api_client.get(
            "/api/v0/generating/text-to-image",
            params={"text": "some text"},
            headers={"Authorization": "Bearer mocked_token"},
        )

        assert response.status_code == 200
        assert response.json() == {}
        setup_jwt_bearer.assert_called_once()
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test__generate_random_video__success(self, mocker, api_client, setup_jwt_bearer):
        mock_execute = mocker.patch.object(
            GenerateRandomVideoUseCase,
            "execute",
            new_callable=AsyncMock,
            return_value=GenerateRandomVideoUseCase.Response(),
        )

        response = await api_client.get(
            "/api/v0/generating/random-video",
            headers={"Authorization": "Bearer mocked_token"},
        )

        assert response.status_code == 200
        assert response.json() == {}
        setup_jwt_bearer.assert_called_once()
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test__generate_random_image__success(self, mocker, api_client, setup_jwt_bearer):
        mock_execute = mocker.patch.object(
            GenerateRandomImageUseCase,
            "execute",
            new_callable=AsyncMock,
            return_value=GenerateRandomImageUseCase.Response(),
        )

        response = await api_client.get(
            "/api/v0/generating/random-image",
            headers={"Authorization": "Bearer mocked_token"},
        )

        assert response.status_code == 200
        assert response.json() == {}
        setup_jwt_bearer.assert_called_once()
        mock_execute.assert_called_once()
