from src.config import get_settings


def get_absolute_url(
    path: str = "",
) -> str:
    conf = get_settings()
    path = path.lstrip("/")
    return f"{conf.application.url_scheme}://{conf.application.hostname}/{path}"
