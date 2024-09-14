import subprocess
import time
import pytest

from fixtures import script_path, sleep_tests


def test_exec_echo(script_path):
    result = subprocess.run(
        ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'exec',
         'echo \'Hello World!\''],
        capture_output=True, text=True
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    assert stderr == "", f"Unexpected stderr: {stderr}"  # Errors?
    assert stdout == "Hello World!", f"Unexpected stdout: {stdout}"  # Output?


@pytest.mark.parametrize("interval,tolerance", sleep_tests)
def test_exec_sleep(interval, tolerance, script_path):
    """Sleep for an interval of time, with a small accepted tolerance, and echo a message; Measure time and output"""
    start_time = time.time()
    result = subprocess.run(
        ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'exec',
         f'sh -c "sleep {interval}; echo \'Hello World!\'"'],
        capture_output=True, text=True
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    assert stderr == "", f"Unexpected stderr: {stderr}"  # Errors?
    assert interval <= elapsed_time <= interval + tolerance, f'Expected elapsed time to be within range, got {elapsed_time}'  # Elapsed Time?
    assert stdout == "Hello World!", f"Unexpected stdout: {stdout}"  # Output?


def test_exec_curl(script_path):
    """Fetch a URL, and make sure we receive a valid result"""
    result = subprocess.run(
        ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'exec',
         'curl -s -o /dev/null -w "%{http_code}" https://www.google.com'],
        capture_output=True, text=True
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    assert stdout == "200", f"Unexpected HTTP status code: {stdout}"
    assert stderr == "", f"Unexpected stderr: {stderr}"
