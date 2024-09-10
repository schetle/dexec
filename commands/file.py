from commands.exec import Exec


class File:
    """Output the contents of a file or files within the context of the container."""

    def __init__(self, container, args, disable_stream, disable_spinner):
        # supported only on somewhat modern posix containers
        # todo: support other systems
        Exec(container, f'cat {args}', disable_stream, disable_spinner)
