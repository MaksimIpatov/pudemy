from urllib.parse import ParseResult, urlparse

from rest_framework.exceptions import ValidationError


class VideoUrlValidator:
    """Валидатор для проверки, что ссылка на видео ведет только на YouTube."""

    AVAILABLE_RESOURCES: tuple[str, ...] = (
        "www.youtube.com",
        "youtube.com",
    )

    def __init__(self, field: str) -> None:
        self._field = field

    def __call__(self, data: dict[str, str]) -> None:
        self._is_valid_video_url(data.get(self._field))

    def _is_valid_video_url(self, value: str) -> None:
        parsed_url: ParseResult = urlparse(value)

        if parsed_url.netloc not in self.AVAILABLE_RESOURCES:
            raise ValidationError("Разрешены только ссылки с YouTube")
