# dexec
Run operations within the context of a running docker container.

## Requirements & Installation
* Python >= 3.11 (tested on 3.11)
* Requirements listed in requirements.txt

Ideally, in a virtual environment:
```bash
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

Make sure you have a valid container, such as:
```bash
docker run --name my-container -dp 80:80 docker/getting-started 
```

## Usage:
`python main.py [options] CONTAINER_NAME COMMAND ARGS...`

## Commands:
  * `exec`: Executes a command within the context of the container.
  * `file`: Output the contents of a file or files within the context of the container.
  * `ls`: Output the contents of a directory within the context of the container.

## Options:
* `--disable_stream`: collect all execution output and output it to stdout at once; the default behavior is to stream the output
* `--disable_spinner`: don't show the activity indicator while processing

## Adding new commands:
To add new commands
* Creating a simple class or function that accepts a container object, and args parameter
* Ensuring your docstring is filled out for the automatically generated help text
* Declaring the command in the "commands" dictionary in main.py

## Explanation
This utility utilizes Docker SDK for Python [Docker SDK for Python](https://github.com/docker/docker-py) to interact with docker's API, on either the unix or tcp sockets. 

The core functionality relies on the `exec_run` method from the Docker SDK. For the `exec` command, `exec_run` executes a command and streams results to stdout. Alternatively, it can output results all at once without streaming.

The `file` and `ls` commands use `exec` to execute the tools `cat` and `ls` within the container. These commands are currently supported only on Unix-like operating systems. On non-Unix systems, you may need to use equivalent commands via the `exec` command.


A simple activity spinner is implemented to indicate work being done in the case of long-running work.

## Alternative Implementation
An alternative to using the Docker SDK is to:

* Implement your own client to interact with Docker's API over sockets (similar to the SDK).
* Use Python's `subprocess` module to interact with Docker via Docker's CLI, which might offer slight performance benefits.


## Examples:
Echo a message
```bash
python main.py my-container echo "Hello World!"
```

Fetch a URL with cURL in a multi-line command
```bash
python main.py my-container exec curl \
https://www.google.com
```

List the contents of the /etc directory
```bash
python main.py my-container ls /etc
```

Get the contents of multiple files
```bash
python main.py my-container file /etc/resolv.conf /etc/udhcpd.conf
```

Redirect the output of a container command to a local file
```bash
python main.py my-container exec date > container_date.txt
```

## Design Considerations
### Complexity:
The time complexity is O(T), where T represents the time required for the command to execute inside the Docker container in addition to the overhead for posting JSON via the Docker API.

Output streaming: O(n), where n is the number of output lines from the command.

### Parallelization:

The activity indicator (or spinner) runs on a separate thread but doesn't introduce any parallel computation for command
execution or output processing.

Potential improvements in parallelization could involve processing commands and their related streamed output in parallel
in the event multiple command support is required and implemented.


### Time Efficiency:

The script's time efficiency primarily depends on the command executed within the Docker container. For complex or I/O-intensive commands, execution time will naturally take longer than that of lightweight commands. The overhead from Docker API interactions and output streaming is minimal and does not significantly impact overall performance.

### Benchmark
The `benchmark.py` file benchmarks the script's execution time and compares it with running Docker's CLI `docker exec`.

```bash
python benchmark.py -c1 "python main.py my-container exec cat /etc/resolv.conf" -c2 "docker exec my-container cat /etc/resolv.conf"
```

| command              | docker exec | dexec      |
|----------------------|-------------|------------|
| date                 | 76.102 ms   | 268.102 ms |
| cat /etc/resolv.conf | 78.425 ms   | 255.685 ms |