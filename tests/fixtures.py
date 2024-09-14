import os
import subprocess
import pytest

sleep_tests = [
    (5, 1),
    (10, 1)
]


@pytest.fixture(scope='session')
def script_path():
    path = os.path.dirname(os.path.abspath(__file__))
    main_script_path = os.path.join(path, "..", "main.py")
    return main_script_path


@pytest.fixture(scope="session")
def exec_create_file(script_path):
    """Create a file, returning the file path and expected contents"""
    cleaned_up = False
    file_path = "/tmp/test.txt"
    contents = "Line1\nLine2\nLine3"

    # create our file
    create_result = subprocess.run(
        ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'exec',
         f'sh -c "echo \'{contents}\' > {file_path}"'],
        capture_output=True, text=True
    )

    stdout = create_result.stdout.strip()
    stderr = create_result.stdout.strip()
    assert stderr == "", f"Unable to create fixture file due to an error, {stderr}"

    # We can call this function later, if we decided to yield the results and perform cleanup
    def does_file_exist():
        # run a check to make sure our tmp file exists
        result = subprocess.run(
            ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'exec',
             'sh -c "test -f /tmp/test.txt && echo 1"'],
            capture_output=True, text=True
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        assert stderr == "", f"Unable to determine file existence in fixture due to an error, {stderr}"
        return stdout == "1"

    assert does_file_exist(), f"Unable to create file {file_path}"

    return {
        "path": file_path,
        "contents": contents
    }
