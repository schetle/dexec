import click
import docker

from commands.dir import ListDirectory
from commands.exec import Exec
from commands.file import File

# list of commands that we support, add new commands as needed
commands = {
    'exec': Exec,
    'file': File,
    'ls': ListDirectory
}


def get_help_text():
    """Generate some friendly help text"""

    text = f'\n\b\nRun operations within the context of a running docker container.\n\b\nCurrent Commands'
    for command in commands:
        text += f'\n{command}: {commands[command].__doc__}'
    return text


def get_container(container_name):
    """Attempt to get a sane docker environment, and container from the passed in container name"""

    client = None
    try:
        # try to get a valid docker client
        client = docker.from_env(timeout=2)
    except Exception as e:
        print(f'Error creating docker client: {e}')
        return None

    container = None
    try:
        # try to locate our desired container
        container = next((c for c in client.containers.list(all=True) if c.name == container_name), None)
        if not container:
            print(f'Container \'{container_name}\' not found')
            return None

        # determine run state. We only operate on currently running containers
        if container.status != 'running':
            print(f'Container \'{container_name}\' not running')
            return None
    except Exception as e:
        print(f'Error retrieving container information: {e}')
        return None

    return container


@click.command(help=get_help_text())
@click.argument('container_name', required=True)  # name of the container we're operating on
@click.argument('command', required=True)  # command we're going to use, listed in 'commands'
@click.argument('args', required=True, nargs=-1)  # arguments being passed into the selected command
@click.option('--disable_stream', is_flag=True, default=False, help="Disabling output streaming; collecting output and writing it all at once")
@click.option('--disable_spinner', is_flag=True, default=False, help="Disable the spinner during long running tasks")
def main(container_name, command, args, disable_stream, disable_spinner):

    # determine if our command is valid
    if command not in commands:
        print(f'Action \'{command}\' not supported')
        return

    # grab our container
    container = get_container(container_name)
    if container is None:
        return

    # clean up our args
    args = ' '.join(args)

    try:
        # run our selected action
        commands[command](container, args, disable_stream, disable_spinner)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
