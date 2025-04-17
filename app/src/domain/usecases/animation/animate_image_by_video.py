import httpx
from fastapi import UploadFile
from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import ResponseFailure
from src.domain.interfaces import IUseCase
from src.infrastructure.configs import MLEngineConfig
from src.infrastructure.exceptions.exceptions import MLEngineException
from src.infrastructure.repositories import (
    SubscriptionRepository,
    UserRepository,
)
from starlette.responses import JSONResponse, StreamingResponse


class AnimateImageByVideoUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo
        source_image: UploadFile
        driving_video: UploadFile

    def __init__(self):
        self.ml_engine_config = MLEngineConfig()
        self.user_repository = UserRepository()
        self.subscription_repository = SubscriptionRepository()

    async def execute(self, request: Request) -> StreamingResponse | JSONResponse:
        try:
            source_image = request.source_image
            driving_video = request.driving_video
            files = {
                "source_image": (source_image.filename, await source_image.read(), source_image.content_type),
                "driving_video": (driving_video.filename, await driving_video.read(), driving_video.content_type),
            }
            async with self.user_repository as repository:
                user = await repository.get_user_by_username(request.user.sub_id)
                user_id = user.id

            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(
                    f"{self.ml_engine_config.BASE_URL}/api/fomm/video",
                    files=files,
                    headers={"X-ML-Engine-Key": self.ml_engine_config.ML_ENGINE_KEY},
                )
                if response.status_code != 200:
                    detail = await response.aread()
                    raise MLEngineException(detail.decode())

                async with self.subscription_repository as repository:
                    subscription = await repository.get_one_by_user_id(user_id=user_id)
                    await repository.update_one(
                        existing_subscription=subscription,
                        queries=-1,
                    )

                return StreamingResponse(response.aiter_bytes(), media_type="video/mp4")

        except Exception as exc:
            return ResponseFailure.build(exc)
