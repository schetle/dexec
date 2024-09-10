from commands.exec import Exec


class ListDirectory:
    """Output the contents of a directory within the context of the container."""

    def __init__(self, container, args, disable_stream, disable_spinner):
        # supported only on somewhat modern posix containers
        # todo: support other systems
        Exec(container, f'ls -alhF {args}', disable_stream, disable_spinner)
