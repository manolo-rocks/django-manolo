from uvicorn.workers import UvicornWorker as BaseUvicornWorker


class UvicornWorkerLifeSpanOff(BaseUvicornWorker):
    """Subclassing UvicornWorker to use the option --lifespan=off that cannot
    be set in the docker files using the gunicorn command.

    This is needed to avoid raising the exception ValueError:

    Django can only handle ASGI/HTTP connections, not lifespan.

    See more details: https://github.com/encode/uvicorn/issues/709
    """
    CONFIG_KWARGS = {"loop": "auto", "http": "auto", "lifespan": "off"}
