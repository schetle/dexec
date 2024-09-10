import io
import sys
from yaspin import yaspin


class Exec:
    """Executes a command within the context of the container."""

    def __init__(self, container, args, disable_stream, disable_spinner):
        self.use_stream = not disable_stream

        self.enable_spinner = not disable_spinner
        self.spinner_message = 'Running'
        self.container = container
        self.args = args
        self.start()

    def start(self):
        # we'll show some progress using yaspin if enabled, which really only matters on longer running tasks
        spinner = None
        if self.enable_spinner:
            spinner = yaspin(text=self.spinner_message)
            spinner.start()

        try:
            # run our command and work through the stream
            if self.use_stream:
                exec_stream = self.container.exec_run(self.args, stream=True)

                first_line = True
                for line in exec_stream.output:

                    # we want to ensure we clear our spinner on the first line, otherwise we'll have a remaining
                    # spin message in the output
                    if first_line:
                        sys.stdout.write(f'\r{" " * (len(self.spinner_message) + 2)}\r')
                        first_line = False

                    # stream the output to stdout
                    sys.stdout.write(line.decode("utf-8"))
                    sys.stdout.flush()
            else:
                code, result = self.container.exec_run(self.args, stream=False)
                sys.stdout.write(result.decode("utf-8"))
                sys.stdout.flush()

        except Exception as e:
            print(e)
        finally:
            if spinner:
                spinner.stop()

