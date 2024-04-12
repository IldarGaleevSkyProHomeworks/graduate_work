from src import config


def get_absolute_url(
    path: str = "",
) -> str:
    conf = config.get_settings()
    path = path.lstrip("/")
    return f"{conf.application.url_scheme}://{conf.application.hostname}/{path}"
